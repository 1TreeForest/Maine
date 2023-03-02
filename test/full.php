<?php

function function1() {
    // while loop
    $i = 1;
    while ($i <= 10) {
        echo "The number is " . $i . "<br>";
        $i++;
    }
    // if-else statement
    $a = 5;
    $b = 10;
    if ($a > $b) {
        echo "a is greater than b";
    } else {
        echo "a is not greater than b";
    }
    // switch statement
    $x = "red";
    switch ($x) {
        case "red":
            echo "Your favorite color is red!";
            break;
        case "blue":
            echo "Your favorite color is blue!";
            break;
        case "green":
            echo "Your favorite color is green!";
            break;
        default:
            echo "Your favorite color is neither red, blue, nor green!";
    }
}

function function2() {
    // do-while loop
    $i = 0;
    do {
        echo $i;
        $i++;
    } while ($i < 10);
    // for loop
    for ($i = 0; $i < 5; $i++) {
        echo $i;
    }
}

function function3() {
    // foreach loop
    $colors = array("red", "green", "blue");
    foreach ($colors as $value) {
        echo "$value <br>";
    }
    // calling another function
    function2();
}

// calling two functions from another function
function main() {
    function1();
    function3();
}

// calling main function
main();

?>
