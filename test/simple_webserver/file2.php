<?php
    require_once 'coverage.php';
    class File2 {
        function process_input2($input){
            $input = strip_tags($input);
            eval($input);
        }
    }
