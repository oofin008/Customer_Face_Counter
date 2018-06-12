<?php
$dsn = getenv('MYSQL_DSN');
$user = getenv('MYSQL_USER');
$password = getenv('MYSQL_PASSWORD');

if(!isset($dsn, $user) || false === $password) {
	throw new Exception('ERRORRRRRR');
}

$db = new PDO($dsn, $user, $password);

//Show all data from customerData table
$statement = $db->prepare("SELECT * FROM customerData");
$statement->execute();
$all = $statement->fetchAll();

//Print out
echo "<center><table id='BGtext'>
                <tr>
                    <th>ID</th>
                    <th>face_id</th>
                    <th>link</th>
					<td>Image</th>
                    <th>counting</th>
                </tr>";

foreach($all as $data){
	echo "<tr>";
	echo "<td>".$data["ID"]."</td>";
	echo "<td>".$data["face_id"]."</td>";
	echo "<td>".$data["link"]."</td>";
	echo "<td><img class='card-img-top' src='https://" .$data["link"]. "' alt='image'></td>";
	echo "<td>".$data["counting"]."</td>";
	echo "</tr>";
}
echo "</table></center>";

?>