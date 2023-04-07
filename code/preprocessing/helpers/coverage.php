<?php

// 启用 Xdebug 的覆盖率收集功能
xdebug_start_code_coverage();

// 在脚本执行结束后获取覆盖率数据
function getCoverage() {
    chdir('/var/www/html/tmp/coverage');
    
    $coverage = xdebug_get_code_coverage();
    
    // 获取test_input的信息
    $seed_id = isset($_REQUEST['seed_id']) ? $_REQUEST['seed_id'] : null;

    $test_input = array(
        'seed_id' => $seed_id,
        );
    
    // 拼接要存储的数据
    $data_to_save = array(
        'test_input' => $test_input,
        
        'coverage' => $coverage,
    );
    
    // 生成保存文件的文件名
    // $filename = basename($_SERVER['SCRIPT_FILENAME']) . '.' . microtime(true) . '.json';
    $filename = microtime(true) . '.json';

    // 将测试数据和覆盖率数据保存为 JSON 格式并写入文件
    file_put_contents($filename, json_encode($data_to_save, JSON_PRETTY_PRINT));

    echo 'Coverage data saved to /var/www/html/tmp/coverage/' . $filename . PHP_EOL;

    $current_dir = getcwd();
    echo $current_dir;
}

register_shutdown_function('getCoverage');
?>
