<?
        if (1)
            if (2)
                echo 3;
            else
                echo 4;
        else
            echo 5;
        if ($a < $b) {
            return -1;
        } elseif ($a > $b) {
            return 1;
        } elseif ($a == $b) {
            return 0;
        } else {
            return 'firetruck';
        }
        if ($if):
            echo 'a';
            echo 'aa';
        elseif ($elseif):
            echo 'b';
        else:
            echo 'c';
        endif;
    ?>