# Special rules for downloading
specials = {'.*/(.*mp4)': 'mess',
            'zjx/303/(.*)': '哈哈哈',
            'zjp/(.*)': '地理',
            'xmh/(.*mp3)': '英语\听力',
            'xmh/(.*xls)': '英语\统计',
            'xmh/(.*)': '英语\课件',
            'ysh/(.*)': '地理',
            'czw/(.*)': '英语',
            'sgf/(.*)': '技术',
            'zzx/(.*)': ''}
# The root directory to store the file
LOCAL_PREFIX = r'D:\Desktop\\'
# The text to display in the window and the coresponding user name
USERS = {'语文': 'zm',
         '数学': 'cjun',
         '英语': 'xmh',
         '陈忠伟': 'czw',
         '化学': 'zjx',
         '钟志兴': 'zzx',
         '团委': 'tgtw',
         '物理': 'zxs',
         '地理杨': 'ysh',
         '地理周': 'zjp',
         '沈国飞': 'sgf',
        }
# The special passwords
PASSWORDS = {'zzx': '1234'}
# Style to adopt
STYLE = 'MaterialBlue'
# The FTP server
SERVER = COMPLEATE_SERVER =  '6.163.193.243:21'
# The encoding of your FTP server
ENCODING = 'gbk'
# Default password for all users
DEFAULT_PASS = '123'
# The size of the file below which to to download silently
SILENT = 2 * 1024 **2
