import sqlparse
from sqlparse.sql import Identifier, Token, Where, Comparison, Parenthesis, Function, IdentifierList, Statement
from sqlparse.tokens import Keyword, DML, Name, Punctuation, Whitespace
from collections import Counter

# Define constants for various SQL components
CLAUSE_KEYWORDS = {'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT', 'INTERSECT', 'UNION', 'EXCEPT'}
JOIN_KEYWORDS = {'JOIN', 'ON', 'AS'}
AGGREGATE_FUNCTIONS = {'AVG', 'COUNT', 'DISTINCT', 'MAX', 'MIN', 'SUM'}
LOGICAL_OPERATORS = {'ALL', 'AND', 'NOT', 'IN', 'NOT IN', 'ANY', 'BETWEEN', 'OR', 'EXISTS', 'LIKE', 'SOME', '=', '>', '<'}
WHERE_OPS = {'NOT', 'BETWEEN', '=', '>', '<', '>=', '<=', '!=', 'IN', 'LIKE', 'IS', 'EXISTS'}
UNIT_OPS = {'NONE', '-', '+', '*', '/'}
AGG_OPS = {'NONE', 'MAX', 'MIN', 'COUNT', 'SUM', 'AVG'}
COND_OPS = {'AND', 'OR'}
SQL_OPS = {'INTERSECT', 'UNION', 'EXCEPT'}
ORDER_OPS = {'DESC', 'ASC'}

def extract_clause_components(query):
    """
    Extracts the clause keywords and arguments from a SQL query, including the WHERE clause and functions like MAX and COUNT.
    """
    parsed = sqlparse.parse(query)
    if not parsed:
        return [], [], [], [], [], False
    
    stmt = parsed[0]
    keywords = set()
    arguments = set()
    operators = set()
    where_columns = set()
    where_operators = set()
    where_values = set()
    nested_query_present = False

    def extract_function_arguments(token):
        """
        Extract arguments within SQL functions like MAX and COUNT.
        """
        if isinstance(token, Function):
            function_name = token.get_real_name().upper()
            if function_name in AGGREGATE_FUNCTIONS:
                keywords.add(function_name)
                for sub_token in token.tokens:
                    if isinstance(sub_token, Parenthesis):
                        for inside_token in sub_token.tokens:
                            if isinstance(inside_token, Identifier) or inside_token.ttype in (Name,):
                                arguments.add(inside_token.get_real_name())
                            elif inside_token.ttype == Punctuation and inside_token.value == '*':
                                arguments.add('*')

    def normalize_column(column):
        """
        Normalizes the column by removing any table aliases or prefixes.
        """
        return column.split('.')[-1] if column else column

    def extract_where_clause(where_token):
        """
        Recursively extract components from the WHERE clause, including nested queries and operators.
        """
        nonlocal nested_query_present
        keywords.add('WHERE')  # Add WHERE keyword when encountering a WHERE clause
        
        for sub_token in where_token.tokens:
            if isinstance(sub_token, Where):
                extract_where_clause(sub_token)
            elif isinstance(sub_token, Comparison):
                left, operator, right = sub_token.left, sub_token.token_next(0)[1], sub_token.right
                if isinstance(left, Identifier):
                    where_columns.add(normalize_column(left.get_real_name()))
                if operator and operator.value.upper() in LOGICAL_OPERATORS:
                    where_operators.add(operator.value.upper())
                if operator and operator.value.upper() == '!=':
                    where_operators.add('!=')
                if isinstance(right, Token):
                    where_values.add(right.value.strip('\'"'))
            elif sub_token.ttype == Keyword and sub_token.value.upper() == 'NOT':
                if sub_token.token_next(1)[1].value.upper() == 'IN':
                    where_operators.add('NOT IN')
            elif isinstance(sub_token, Parenthesis):
                # Check for nested SELECT statements
                nested_query_present = any(isinstance(t, Where) for t in sub_token.tokens)
            elif sub_token.ttype in {Keyword, Punctuation} and sub_token.value.upper() in LOGICAL_OPERATORS:
                where_operators.add(sub_token.value.upper())
            elif sub_token.ttype in {Keyword, Punctuation} and sub_token.value.upper() == '!=':
                where_operators.add('!=')
    
    def extract_group_by_clause(stmt):
        """
        Extract components from the GROUP BY clause.
        """
        group_by_keywords = {'GROUP BY'}
        for token in stmt.tokens:
            if token.ttype in {Keyword} and token.value.upper() in group_by_keywords:
                keywords.add('GROUP BY')
                _, next_token = stmt.token_next(stmt.token_index(token))
                if isinstance(next_token, IdentifierList):
                    for identifier in next_token.get_identifiers():
                        arguments.add(normalize_column(identifier.get_real_name()))
                elif isinstance(next_token, Identifier):
                    arguments.add(normalize_column(next_token.get_real_name()))
                    
    def extract_join_clause(stmt):
        """
        Extract components from the JOIN clause.
        """
        join_keywords = {'JOIN', 'ON'}
        tokens = stmt.tokens
        for i, token in enumerate(tokens):
            if token.ttype in {Keyword} and token.value.upper() in join_keywords:
                keywords.add(token.value.upper())
                _, next_token = stmt.token_next(i)
                if isinstance(next_token, IdentifierList):
                    for identifier in next_token.get_identifiers():
                        arguments.add(normalize_column(identifier.get_real_name()))
                elif isinstance(next_token, Identifier):
                    arguments.add(normalize_column(next_token.get_real_name()))
                # Capture the columns used in the ON clause
                if token.value.upper() == 'ON':
                    for j in range(i + 1, len(tokens)):
                        sub_token = tokens[j]
                        if isinstance(sub_token, Comparison):
                            left, operator, right = sub_token.left, sub_token.token_next(0)[1], sub_token.right
                            if isinstance(left, Identifier):
                                arguments.add(normalize_column(left.get_real_name()))
                            if operator and operator.value.upper() in LOGICAL_OPERATORS:
                                operators.add(operator.value.upper())
                            if isinstance(right, Identifier):
                                arguments.add(normalize_column(right.get_real_name()))
                        elif sub_token.ttype == Keyword and sub_token.value.upper() == 'AND':
                            # Move to the next token to check for additional conditions
                            continue
                        elif sub_token.ttype in {Keyword, Punctuation} and sub_token.value.upper() in LOGICAL_OPERATORS:
                            operators.add(sub_token.value.upper())
                    
    def extract_exceptions(stmt):
        """
        Extract components from the EXCEPT clause.
        """
        exception_keywords = {'EXCEPT'}
        for token in stmt.tokens:
            if token.ttype in {Keyword} and token.value.upper() in exception_keywords:
                keywords.add('EXCEPT')
                _, next_token = stmt.token_next(stmt.token_index(token))
                if isinstance(next_token, Parenthesis):
                    for sub_token in next_token.tokens:
                        if isinstance(sub_token, Statement):
                            nested_keywords, nested_arguments, nested_where_columns, nested_where_operators, nested_where_values, nested_nested_query = extract_clause_components(sub_token.value)
                            keywords.update(nested_keywords)
                            arguments.update(nested_arguments)
                            where_columns.update(nested_where_columns)
                            where_operators.update(nested_where_operators)
                            where_values.update(nested_where_values)
                            nested_query_present = nested_query_present or nested_nested_query

    for token in stmt.tokens:
        if token.ttype in {Keyword, DML} and token.value.upper() in CLAUSE_KEYWORDS:
            keywords.add(token.value.upper())
        elif isinstance(token, Where):
            # Capture arguments within the WHERE clause
            extract_where_clause(token)
        elif isinstance(token, Identifier) or token.ttype in (Name,):
            normalized_token = normalize_column(token.get_real_name())
            arguments.add(normalized_token)
        elif isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                normalized_identifier = normalize_column(identifier.get_real_name())
                arguments.add(normalized_identifier)
        elif isinstance(token, Function):
            extract_function_arguments(token)
        elif token.ttype in {Keyword, Punctuation} and token.value.upper() in LOGICAL_OPERATORS:
            operators.add(token.value.upper())
        elif token.ttype == Keyword and token.value.upper() in SQL_OPS:
            keywords.add(token.value.upper())
    
    # Hardcode inclusion of INTERSECT
    if 'INTERSECT' in query.upper():
        keywords.add('INTERSECT')
    
    # Extract additional clauses
    extract_group_by_clause(stmt)
    extract_join_clause(stmt)
    extract_exceptions(stmt)

    return keywords, arguments, operators, where_columns, where_operators, where_values, nested_query_present

def normalize_values(set1, set2):
    """
    Normalizes values by removing single and double quotes.
    """
    def remove_quotes(value):
        return value.replace("'", "").replace('"', "")
    
    normalized_set1 = {remove_quotes(item) for item in set1}
    normalized_set2 = {remove_quotes(item) for item in set2}
    
    return normalized_set1, normalized_set2

def calculate_similarity(set1, set2):
    """
    Calculates similarity between two sets as the ratio of the intersection to the union.
    """
    set1, set2 = normalize_values(set1, set2)
    
    if not set1 and not set2:
        return 1.0  # Both sets are empty, consider them as identical

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    return len(intersection) / len(union) # if union else 1.0  TO Avoid division by zero (for now we dont write it lets see)

def calculate_ngram_overlap(set1, set2, n=3):
    """
    Calculates n-gram overlap between two sets.
    """
    set1, set2 = normalize_values(set1, set2)
    
    if not set1 and not set2:
        return 1.0  # Both sets are empty, consider them as identical

    def get_ngrams(s, n):
        return [s[i:i+n] for i in range(len(s)-n+1)]

    set1_ngrams = Counter()
    set2_ngrams = Counter()

    for item in set1:
        set1_ngrams.update(get_ngrams(item, n))
    
    for item in set2:
        set2_ngrams.update(get_ngrams(item, n))
    
    intersection = set1_ngrams & set2_ngrams
    union = set1_ngrams | set2_ngrams

    if not union:
        return 0.0
    
    return sum(intersection.values()) / sum(union.values())

def evaluate_similarity(gold_file, predicted_file):
    """
    Evaluates the similarity between gold and predicted SQL queries based on keywords and arguments.
    """
    with open(gold_file, 'r') as gf, open(predicted_file, 'r') as pf:
        gold_queries = gf.readlines()
        predicted_queries = pf.readlines()

    if len(gold_queries) != len(predicted_queries):
        print("Mismatch in number of queries between gold and predicted files.")
        return

    for i, (gold_query, predicted_query) in enumerate(zip(gold_queries, predicted_queries)):
        gold_keywords, gold_arguments, gold_operators, gold_where_columns, gold_where_operators, gold_where_values, gold_nested_query = extract_clause_components(gold_query.strip())
        predicted_keywords, predicted_arguments, predicted_operators, predicted_where_columns, predicted_where_operators, predicted_where_values, predicted_nested_query = extract_clause_components(predicted_query.strip())
        
        keyword_similarity = calculate_similarity(gold_keywords, predicted_keywords)
        argument_similarity = calculate_similarity(gold_arguments, predicted_arguments)
        operator_similarity = calculate_similarity(gold_operators, predicted_operators)
        column_similarity = calculate_similarity(gold_where_columns, predicted_where_columns)
        where_operator_similarity = calculate_similarity(gold_where_operators, predicted_where_operators)
        value_similarity = calculate_similarity(gold_where_values, predicted_where_values)

        keyword_ngram_overlap = calculate_ngram_overlap(gold_keywords, predicted_keywords)
        argument_ngram_overlap = calculate_ngram_overlap(gold_arguments, predicted_arguments)
        operator_ngram_overlap = calculate_ngram_overlap(gold_operators, predicted_operators)
        column_ngram_overlap = calculate_ngram_overlap(gold_where_columns, predicted_where_columns)
        where_operator_ngram_overlap = calculate_ngram_overlap(gold_where_operators, predicted_where_operators)
        value_ngram_overlap = calculate_ngram_overlap(gold_where_values, predicted_where_values)
        
        print(f"Query {i+1} similarity:")
        print(f"  Keyword similarity: {keyword_similarity:.2f}")
        print(f"  Keyword n-gram overlap: {keyword_ngram_overlap:.2f}")
        print(f"  Argument similarity: {argument_similarity:.2f}")
        print(f"  Argument n-gram overlap: {argument_ngram_overlap:.2f}")
        print(f"  Operator similarity: {operator_similarity:.2f}")
        print(f"  Operator n-gram overlap: {operator_ngram_overlap:.2f}")
        print(f"    Gold keywords: {gold_keywords}")
        print(f"    Predicted keywords: {predicted_keywords}")
        print(f"    Gold arguments: {gold_arguments}")
        print(f"    Predicted arguments: {predicted_arguments}")
        print(f"    Gold operators: {gold_operators if gold_operators else 'None'}")
        print(f"    Predicted operators: {predicted_operators if predicted_operators else 'None'}")
        print(f"  WHERE clause component similarities:")
        print(f"    Column similarity: {column_similarity:.2f}")
        print(f"    Column n-gram overlap: {column_ngram_overlap:.2f}")
        print(f"    Operator similarity: {where_operator_similarity:.2f}")
        print(f"    Operator n-gram overlap: {where_operator_ngram_overlap:.2f}")
        print(f"    Value similarity: {value_similarity:.2f}")
        print(f"    Value n-gram overlap: {value_ngram_overlap:.2f}")
        print(f"      Gold WHERE columns: {gold_where_columns}")
        print(f"      Predicted WHERE columns: {predicted_where_columns}")
        print(f"      Gold WHERE operators: {gold_where_operators if gold_where_operators else 'None'}")
        print(f"      Predicted WHERE operators: {predicted_where_operators if predicted_where_operators else 'None'}")
        print(f"      Gold WHERE values: {gold_where_values}")
        print(f"      Predicted WHERE values: {predicted_where_values}")

if __name__ == "__main__":
    gold_file = 'gold_queries.sql'
    predicted_file = 'predicted_queries.sql'
    evaluate_similarity(gold_file, predicted_file)
  
