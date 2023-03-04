<?php
    class File2 {
        function process_input($input){
            $input = strip_tags($input);
            eval($input);
        }
    }
?>
