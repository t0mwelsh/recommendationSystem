<html>
  <head>
    <title>Book Fetcher</title>
  </head>
  <body>
    <?php
    // Allow cross-origin requests
    /*header("Access-Control-Allow-Origin: http://localhost");
    header("Content-Type: application/json; charset=UTF-8");
    header("Access-Control-Allow-Methods: GET");
    header("Access-Control-Max-Age: 3600");
    header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

    // Check if the request contains the API key
    $providedKey = $_GET['api_key']; // You can change this to the appropriate parameter name

    // Replace 'YOUR_API_KEY' with your actual API key
    $validKey = '09ff24b0-fdcf-4f6e-9beb-7cbef70a49cf';

    // Verify the API key
    if ($providedKey !== $validKey) {
        header('HTTP/1.0 401 Unauthorized');
        echo 'Unauthorized';
        exit;
    }*/

    // Database connection parameters
    $servername = " surus.db.elephantsql.com";
    $username = "nwgmoppd";
    $password = "1vzJoB2_ik_sIHGW9rsyUZA5XAS4cO9l";
    $dbname = "nwgmoppd";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // SQL query to fetch data
    $sql = "SELECT item_name, item_author, image_url FROM books";
    $result = $conn->query($sql);

    // Fetch data as associative array
    $data = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
    }

    // Close the connection
    $conn->close();

    // Set the content type to JSON
    header('Content-Type: application/json');

    // Output the JSON data
    echo json_encode($data);
    ?>
  </body>
</html>