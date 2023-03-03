<?php

// 定义一个包含 if 条件语句的类
class Class_If {
    public function run_if() {
        $x = 10;
        if ($x < 20) {
            echo "This is if statement<br>";
        }
    }
}

// 实例化类并调用方法
$obj = new Class_If();
$obj->run_if();

// 包含另一个文件
include_once 'test/file_include_1.php';

// 实例化另一个文件中的类并调用方法
$obj_while = new Class_While();
$obj_while->run_while();
?>