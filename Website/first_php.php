<?php
$servername = "surus.db.elephantsql.com";
$database = "nwgmoppd";
$username = "nwgmoppd";
$password = "1vzJoB2_ik_sIHGW9rsyUZA5XAS4cO9l";

try {
    $pdo = new PDO("pgsql:host=$servername;dbname=$database", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare('SELECT * FROM your_table LIMIT 10');
    $stmt->execute();

    while ($row = $stmt->fetch()) {
        echo "ID: " . $row['id'] . ", Name: " . $row['name'] . ", Author: " . $row['author'] . "<br>";
    }
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>