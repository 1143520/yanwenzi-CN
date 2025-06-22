#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
颜文字字符修复脚本
检查和修复颜文字中的字符编码问题
"""

import json
import os
import re

def check_and_fix_kaomoji_file(file_path):
    """检查并修复kaomoji.js文件中的字符问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 记录修复
        fixes = []
        
        # 修复常见的字符问题
        fixes_map = {
            # 修复点号替换问题
            '(.ﾟ∀.ﾟ)': '(ﾟ∀ﾟ)',
            '(.ﾟ∀.ﾟ)o彡ﾟ': '( ﾟ∀ﾟ)o彡ﾟ',
            
            # 修复其他可能的Unicode问题
            '（ﾟ∀ﾟ）': '(ﾟ∀ﾟ)',  # 全角括号转半角
            '（': '(',
            '）': ')',
            '｛': '{',
            '｝': '}',
            '［': '[',
            '］': ']',
        }
        
        original_content = content
        
        for wrong, correct in fixes_map.items():
            if wrong in content:
                content = content.replace(wrong, correct)
                fixes.append(f"修复: '{wrong}' -> '{correct}'")
        
        # 检查特殊字符
        problematic_chars = []
        for line_num, line in enumerate(content.split('\n'), 1):
            if '"' in line and ('ﾟ' in line or '∀' in line):
                # 提取颜文字
                matches = re.findall(r'"([^"]*[ﾟ∀][^"]*)"', line)
                for match in matches:
                    # 检查是否有异常字符
                    if '.' in match and 'ﾟ' in match:
                        problematic_chars.append(f"行 {line_num}: {match}")
        
        if content != original_content:
            # 备份原文件
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # 保存修复后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 文件已修复: {file_path}")
            print(f"📁 备份文件: {backup_path}")
            for fix in fixes:
                print(f"  {fix}")
        else:
            print(f"✅ 文件无需修复: {file_path}")
        
        if problematic_chars:
            print("\n⚠️  发现可能有问题的字符:")
            for char in problematic_chars:
                print(f"  {char}")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理文件失败: {e}")
        return False

def check_unicode_support():
    """检查Unicode字符支持"""
    test_chars = [
        '(ﾟ∀ﾟ)',
        '(*´∀`*)',
        '(´▽`ʃ♡ƪ)',
        'ヾ(●゜▽゜●)♡',
        '｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡',
        '∑(ι´Дン)ノ',
        '◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣'
    ]
    
    print("🔍 Unicode字符支持测试:")
    for char in test_chars:
        try:
            # 测试编码和解码
            encoded = char.encode('utf-8')
            decoded = encoded.decode('utf-8')
            if char == decoded:
                print(f"  ✅ {char}")
            else:
                print(f"  ❌ {char} (编码问题)")
        except Exception as e:
            print(f"  ❌ {char} (错误: {e})")

def main():
    """主函数"""
    print("🔧 颜文字字符修复工具")
    print("=" * 50)
    
    # 检查Unicode支持
    check_unicode_support()
    print()
    
    # 修复kaomoji.js文件
    kaomoji_files = [
        "src/assets/kaomoji.js",
        "src/assets/kaomoji_new.js",
        "src/assets/kaomoji_all_in_one.js"
    ]
    
    for file_path in kaomoji_files:
        if os.path.exists(file_path):
            print(f"📂 检查文件: {file_path}")
            check_and_fix_kaomoji_file(file_path)
            print()
        else:
            print(f"⚠️  文件不存在: {file_path}")
    
    print("🎉 检查完成!")

if __name__ == "__main__":
    main()
