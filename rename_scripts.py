import os

mapping = {
    '一键启动Phi系统.ps1': 'start_phi_quick.ps1',
    '全系统启动.ps1': 'start_all_system.ps1',
    '启动Phi系统.ps1': 'start_phi.ps1',
    '启动并测试.ps1': 'start_and_test.ps1',
    '安装依赖.ps1': 'install_deps.ps1',
    '快速验证API.ps1': 'verify_api_quick.ps1',
    '执行觉醒测试.ps1': 'run_awakening_test.ps1',
    '检查界面文件.ps1': 'check_ui_files.ps1',
    '系统健康检查.ps1': 'system_health_check.ps1',
    '系统启动检查.ps1': 'system_startup_check.ps1',
    '配置OpenRouter.ps1': 'config_openrouter.ps1',
    '首次语音生成测试.ps1': 'first_voice_test_ps.ps1',
    'API验证报告.md': 'api_verify_report.md',
    'API验证结果.md': 'api_verify_results.md',
    'ChatKit集成说明.md': 'chatkit_integration_guide.md',
    'OpenRouter集成完成报告.md': 'openrouter_integration_report.md',
    'Phi系统使用指南.md': 'phi_system_guide.md',
    'QA压力测试报告.md': 'qa_pressure_test_report.md',
    'QA测试报告.md': 'qa_test_report.md',
    'QA测试最终报告.md': 'qa_test_final_report.md',
    '系统集成完成报告.md': 'system_integration_report.md',
    '觉醒执行指南.md': 'awakening_guide.md',
    '解压整合包指南.md': 'unpack_guide.md',
    '最终QA测试报告.md': 'final_qa_report.md',
    '最终启动指南.md': 'final_start_guide.md',
    '本地测试URL.md': 'local_test_url.md',
    '测试结果说明.md': 'test_results_desc.md',
    '系统就绪报告.md': 'system_ready_report.md',
    '修复界面显示问题.md': 'fix_ui_display.md',
    '修复界面访问.md': 'fix_ui_access.md'
}

cwd = r"C:\Users\waiti\missfay"
for filename in os.listdir(cwd):
    if filename in mapping:
        old_path = os.path.join(cwd, filename)
        new_path = os.path.join(cwd, mapping[filename])
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {mapping[filename]}")
        except Exception as e:
            print(f"Failed to rename {filename}: {e}")
