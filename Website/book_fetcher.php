<?php

$servername = "surus.db.elephantsql.com";
$database = "nwgmoppd";
$username = "nwgmoppd";
$password = "1vzJoB2_ik_sIHGW9rsyUZA5XAS4cO9l";

try {
    $pdo = new PDO("pgsql:host=$servername;dbname=$database", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare('SELECT item_name, item_author, image_url FROM books');
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Handle null values
    foreach ($data as &$row) {
        foreach ($row as $key => $value) {
            if ($value === null) {
                $row[$key] = ''; // Replace null with an empty string
            }
        }
    }

    header('Content-Type: application/json');
    echo json_encode($data);
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
