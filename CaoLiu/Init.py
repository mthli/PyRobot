# python标准库
import os
# python第三方库
import dropbox

# 填写自己的Dropbox App key和Dropbox App secret
APP_KEY = ''
APP_SECRET = ''

# 开始登陆
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(
        APP_KEY,
        APP_SECRET
        )
authorize_url = flow.start()

# 取得认证信息
print('1. Go to: ', authorize_url)
print('2. Click "Allow" (you might have to log in first)')
print('3. Copy the authorization code.')
code = input("Enter the authorization code here: ").strip()
access_token, user_id = flow.finish(code)

# 将取得的认证信息写入文件，方便以后使用
f = open('actid.txt', 'w+')
f.writelines(access_token)
f.writelines('\n')
f.writelines(user_id)
f.close()
