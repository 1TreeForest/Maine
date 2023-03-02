<?php
class ControlStatements {
    public function ifElse($value) {
        if($value > 10) {
            echo "The value is greater than 10";
        } else {
            echo "The value is less than or equal to 10";
        }
    }

    public function whileLoop($start, $end) {
        while($start <= $end) {
            echo $start . " ";
            $start++;
        }
    }

    public function switchCase($value) {
        switch($value) {
            case 1:
                echo "The value is 1";
                break;
            case 2:
                echo "The value is 2";
                break;
            default:
                echo "The value is neither 1 nor 2";
                break;
        }
    }
    
    public function callMethods() {
        $this->ifElse(15);
        $this->whileLoop(1, 5);
        $this->switchCase(3);
    }
}

function test($i) {
    $obj = new ControlStatements();
    $obj->callMethods();
    $test = $i;
}

test(1);
$obj2 = new ControlStatements();
$obj2->callMethods();
?>
