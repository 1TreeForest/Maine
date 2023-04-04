<?php

// 启用 Xdebug 的覆盖率收集功能
xdebug_start_code_coverage();

// 在脚本执行结束后获取覆盖率数据
function getCoverage() {
    $coverage = xdebug_get_code_coverage();
    chdir('/var/www/html/tmp/coverage');

    // 生成保存文件的文件名
    $filename = basename($_SERVER['SCRIPT_FILENAME']) . '.' . microtime(true) . '.json';

    // 将覆盖率数据保存为 JSON 格式并写入文件
    file_put_contents($filename, json_encode($coverage, JSON_PRETTY_PRINT));

    echo 'Coverage data saved to /var/www/html/tmp/coverage/' . $filename . PHP_EOL;

    $current_dir = getcwd();
    echo $current_dir;
}

register_shutdown_function('getCoverage');
?>
