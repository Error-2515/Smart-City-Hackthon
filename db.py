def find_vehicle_owner(image_path, threshold=0.4):
    """
    Finds the owner of a vehicle by processing an image to extract vehicle details
    and searching the database for matching records.

    Parameters:
        image_path (str): Path to the image of the vehicle.
        threshold (float): Minimum similarity ratio for fuzzy matching (default is 0.4).

    Returns:
        tuple: (list of matching vehicle details, number_plate, owner_phone, owner_name, message)
    """
    import mysql.connector
    from Levenshtein import ratio
    import process as pr

    # Database configuration
    db_config = {
        "host": "localhost",
        "user": "",#enter mysql user
        "password": "",#enter mysql password
        "database": "vehicle_db"#mysql database used
    }

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Process the image to extract vehicle details
        color, input_plate, vehicle_type = pr.process_image(image_path)

        # Step 1: Query all number plates for fuzzy matching
        query = """
            SELECT number_plate, owner_name, owner_phone, car_color, vehicle_type
            FROM vehicles
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Step 2: Filter results using fuzzy matching on number plate
        filtered_rows = [row for row in rows if ratio(input_plate, row[0]) >= threshold]

        # If exactly one match is found using number plate, return it immediately
        if len(filtered_rows) == 1:
            row = filtered_rows[0]
            return row[0], row[2], row[1],row[3],row[4], "Single match found (by number plate similarity)."

        # Step 3: If multiple matches exist, filter by color
        filtered_rows = [row for row in filtered_rows if row[3].lower() == color.lower()]
        if len(filtered_rows) == 1:
            row = filtered_rows[0]
            return row[0], row[2], row[1],row[3],row[4], "Single match found (by color)."

        # Step 4: If multiple matches still exist, filter by vehicle type
        filtered_rows = [row for row in filtered_rows if row[4].lower() == vehicle_type.lower()]
        if len(filtered_rows) == 1:
            row = filtered_rows[0]
            return row[0], row[2], row[1],row[3],row[4], "Single match found (by vehicle type)."

        # Step 5: If multiple matches remain, return no result
        if len(filtered_rows) > 1:
            return None, None, None,None,None, "Multiple matches found, unable to determine the exact vehicle."

        return None, None, None,None,None, "No matching vehicles found."

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None, None, None,None,None, "Database error occurred."

    finally:
        # Ensure resources are released
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Example usage (in another Python file):
if __name__ == "__main__":
    image_path = r'Dataset\test\1.jpg'  # Replace with your image path
    number_plate, phone_number, owner_name, output_message = find_vehicle_owner(image_path)

    print(output_message)
    if number_plate and phone_number and owner_name:
        print(f"Number Plate: {number_plate}, Phone Number: {phone_number}, Owner Name: {owner_name}")
