<?php

// 定义一个包含静态方法和动态方法的类
class MyClass {
    public static function staticMethod() {
        echo "This is a static method.\n";
    }

    public function dynamicMethod() {
        echo "This is a dynamic method.\n";
    }
}

// 创建一个类的实例
$obj = new MyClass();

// 调用静态方法
MyClass::staticMethod();

// 调用动态方法
$obj->dynamicMethod();

?>
