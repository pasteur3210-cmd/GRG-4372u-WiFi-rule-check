import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from log_validator import check_log,analyze_log
FIXTURE='''[MES] 字段查询响应：MsgId=0, MsgStr=DIGIFIBRA-rhh0, FieldValue=DIGIFIBRA-rhh0
命令：nvram set WiFiSSIDSuffix rhh0
命令：nvram get WiFiSSIDSuffix
stdout：nvram get WiFiSSIDSuffix
rhh0
[MES]   MES 字段“cst10”读取成功，值：N7^CHsfUGnmw。
命令：nvram set WiFiPwd N7^CHsfUGnmw
命令：nvram get WiFiPwd
stdout：nvram get WiFiPwd
N7^CHsfUGnmw
[系统] 最终结果：成功；状态：测试流程通过。；失败数量：0
'''
class LogTests(unittest.TestCase):
 def test_valid(self):self.assertEqual(check_log(FIXTURE)['status'],'PASS')
 def test_missing_get(self):
  s=FIXTURE.replace('命令：nvram get WiFiPwd\nstdout：nvram get WiFiPwd\nN7^CHsfUGnmw\n','')
  self.assertIn('LOG_MISSING_FIELD',[x['code'] for x in check_log(s)['issues']])
 def test_bad_key(self):
  s=FIXTURE.replace('N7^CHsfUGnmw','N0^CHsfUGnmw')
  self.assertIn('KEY_BANNED_CHARACTER',[x['code'] for x in check_log(s)['issues']])
 def test_written_differs(self):
  s=FIXTURE.replace('命令：nvram set WiFiSSIDSuffix rhh0','命令：nvram set WiFiSSIDSuffix abc3')
  self.assertIn('SSID_WRITE_MISMATCH',[x['code'] for x in check_log(s)['issues']])
 def test_key_mismatch(self):
  s=FIXTURE.replace('命令：nvram set WiFiPwd N7^CHsfUGnmw','命令：nvram set WiFiPwd K7m!R4t%H5x+')
  self.assertIn('KEY_WRITE_MISMATCH',[x['code'] for x in check_log(s)['issues']])
 def test_run_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'t.log';p.write_text(FIXTURE,encoding='utf-8')
   r=analyze_log(p,d)
   self.assertEqual(r['fail'],0);self.assertTrue(Path(r['report']).exists())
 def test_real_file(self):
  p=Path(__file__).resolve().parents[2]/'信息写入_DT.log'
  if p.exists():
   r=analyze_log(p,tempfile.mkdtemp(prefix='dt_log_check_'))
   self.assertEqual(r['fail'],0,r['errors'])
if __name__=='__main__':unittest.main()
