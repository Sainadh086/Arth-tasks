
<?php
echo "Webpage working on Haproxy LoadBalancer";


echo "<br>";

echo "Ip of the Webserver:".$_SERVER['SERVER_ADDR'] ;
echo "<br>";
echo "<br>";

echo "forwarded from:".$_SERVER['HTTP_X_FORWARDED_FOR'];
echo "<br>";

echo "Thank you for visting the page"
?>
