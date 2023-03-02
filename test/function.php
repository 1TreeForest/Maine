<?php
function functionA() {
  echo "This is Function A.\n";
}

function functionB() {
  echo "This is Function B.\n";
}

function functionC() {
  echo "This is Function C.\n";
  functionA();
  functionB();
}

functionC();
?>
