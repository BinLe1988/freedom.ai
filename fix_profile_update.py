#!/usr/bin/env python3
"""
修复档案更新问题的补丁
Fix for Profile Update Issues
"""

def get_fixed_api_update_profile():
    """返回修复后的API更新档案方法"""
    
    code = '''
    @app.route('/api/update_profile', methods=['POST'])
    @require_login
    def api_update_profile():
        """API: 更新用户档案"""
        try:
            data = request.json
            user_id = session['user_id']
            
            # 更新用户档案
            profile_updates = {}
            for key in ['full_name', 'bio', 'location', 'industry', 'current_role', 'experience_years', 'skills', 'interests']:
                if key in data:
                    profile_updates[key] = data[key]
            
            if profile_updates:
                # 检查用户档案是否存在
                existing_profile = db.get_user_profile(user_id)
                
                if existing_profile is None:
                    # 档案不存在，先创建档案
                    print(f"用户 {user_id} 档案不存在，正在创建...")
                    db.create_user_profile(user_id, **profile_updates)
                    print(f"用户 {user_id} 档案创建成功")
                else:
                    # 档案存在，执行更新
                    success = db.update_user_profile(user_id, **profile_updates)
                    if not success:
                        return jsonify({'success': False, 'error': '档案更新失败'}), 500
                    print(f"用户 {user_id} 档案更新成功")
            
            # 更新用户偏好
            preference_updates = {}
            for key in ['preferred_work_type', 'preferred_job_types', 'salary_expectations', 
                       'location_preferences', 'industry_preferences', 'company_size_preference', 'learning_style']:
                if key in data:
                    preference_updates[key] = data[key]
            
            if preference_updates:
                # 检查用户偏好是否存在
                existing_preferences = db.get_user_preferences(user_id)
                
                if existing_preferences is None:
                    # 偏好不存在，先创建偏好
                    print(f"用户 {user_id} 偏好不存在，正在创建...")
                    db.create_user_preferences(user_id, **preference_updates)
                    print(f"用户 {user_id} 偏好创建成功")
                else:
                    # 偏好存在，执行更新
                    success = db.update_user_preferences(user_id, **preference_updates)
                    if not success:
                        return jsonify({'success': False, 'error': '偏好更新失败'}), 500
                    print(f"用户 {user_id} 偏好更新成功")
            
            # 记录更新行为
            log_user_action(ActionType.PREFERENCE_UPDATE, {
                'updated_fields': list(profile_updates.keys()) + list(preference_updates.keys())
            })
            
            return jsonify({'success': True, 'message': '档案更新成功'})
            
        except Exception as e:
            print(f"档案更新异常: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    '''
    
    return code

if __name__ == "__main__":
    print("修复档案更新的代码:")
    print(get_fixed_api_update_profile())
