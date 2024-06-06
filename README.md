# Generating DIRNDL Instances for `tables.json` and `dev.json`

Given the simplified and smaller version of the DIRNDL database, created by me and available at: [DIRNDL Database](https://drive.google.com/drive/folders/1reK5Lx7EgKV2ooR0cYOrBXOPUOId43lH?usp=drive_link), the first step consists in obtaining the files representing the structure of the database in the formats required by the systems, as outlined in Section 7 of my thesis work. For this purpose, these steps must be followed:

## Steps to Generate `tables.json`

1. **Create a Database Directory:**
   Create a directory named `database` inside `spider/preprocess/`.
   ```sh
   mkdir -p spider/preprocess/database
