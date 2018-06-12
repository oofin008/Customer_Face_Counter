<?php
/**
 * Copyright 2016 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

# [START example]
use Silex\Application;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

// create the Silex application
$app = new Application();

// Create the PDO object for CloudSQL MySQL.
$dsn = getenv('MYSQL_DSN');
$user = getenv('MYSQL_USER');
$password = getenv('MYSQL_PASSWORD');
$pdo = new PDO($dsn, $user, $password);

// Create the database if it doesn't exist
//$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
//$pdo->query('CREATE TABLE IF NOT EXISTS visits ' .
    '(time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, user_ip CHAR(64))');

// Add the PDO object to our Silex application.
$app['pdo'] = $pdo;

$app->get('/', function (Application $app, Request $request) {

    // Insert a visit into the database.
    /** @var PDO $pdo */
    /*$pdo = $app['pdo'];
    $insert = $pdo->prepare('INSERT INTO visits (user_ip) values (:user_ip)');
    $insert->execute(['user_ip' => $user_ip]);*/

    // Look up the last 10 visits
    $select = $pdo->prepare(
        'SELECT * FROM customerData');
    $select->execute();
    $visits = ["Last 10 visits:"];
    while ($row = $select->fetch(PDO::FETCH_ASSOC)) {
        array_push($visits, sprintf('ID: %d  face_id: %s  link: %s  count: %d', $row['ID'],
            $row['face_id'], $row['link'], $row['counting']));
    }
    return new Response(implode("\n", $visits), 200,
        ['Content-Type' => 'text/plain']);
});
# [END example]

return $app;