<?php

// 定义一个包含 while 循环的类
class Class_While {
    public function run_while() {
        $i = 1;
        while ($i <= 10) {
            echo "The number is " . $i . "<br>";
            $i++;
        }
    }
}

// 实例化类并调用方法
$obj = new Class_While();
$obj->run_while();

// 包含另一个文件
include 'test/file_include_2.php';

// 实例化另一个文件中的类并调用方法
$obj_if = new Class_If();
$obj_if->run_if();
?>