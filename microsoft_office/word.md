# Microsoft Word

## Adjusting Total Number of Pages using Field codes

1. Press `Alt + F9` to reveal field codes in the document.
2. Select the entire `{ NUMPAGES }` field, including the braces.
3. Press `Ctrl + F9`: insert a new pair of field code braces: `{  }`
4. Insert the expression as follows:

    ```text
    { = { NUMPAGES } - 1 } # pagenumber minus 1
    ```

5. Press `Alt + F9` again to hide field codes.
6. Select the field and press `F9` to update it, it should now show one less than the total number of pages.
    Note:  Previewing or printing the document can also update the field.
    - In newer Word versions, ensure **File > Options > Display > Update fields before printing** is checked.
    - In older versions, this setting is under **Tools > Options > Print**.

---

## Using Variables in Specific Sections

Define and reuse custom values using Word field codes. This method is useful for reusing calculated values, page counts, or any predefined variables across the Word document.

### Define a Variable

1. Navigate to the desired section.
2. Press `Alt + F9` to view field codes.
3. Press `Ctrl + F9` to insert a field code.
4. Inside the field, type:

    ```text
    SET variableName value
    ```

5. Press `Alt + F9` to hide codes.

### Reference the Variable in Another Section

1. Go to the target section.
2. Press `Alt + F9`, then `Ctrl + F9` to create a field.
3. Type:

    ```text
    = variableName
    ```

4. Press `Alt + F9`, then `F9` to update and display the value.
