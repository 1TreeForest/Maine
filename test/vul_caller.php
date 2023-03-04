<?php

require_once '/home/fuzz/Desktop/Projects/Maine/test/vulnerable.php';

$vulnerable = new VulnerableClass();
echo $vulnerable->login() . "<br>";
echo $vulnerable->getInfo() . "<br>";

$vulnerable->vulnerableFunction();
