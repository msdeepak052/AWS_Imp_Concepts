from flask import Flask, request, redirect
import boto3
import os

app = Flask(__name__)
s3 = boto3.client('s3', region_name='ap-south-1')
BUCKET = os.environ.get('STOREOPS_BUCKET', '<STOREOPS_BUCKET_NAME>')
PREFIX = 'uploads/'

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NorthStar Retail - Store-Ops Photo Uploader</title>
<style>
  :root {{ --aws-orange:#FF9900; --aws-dark:#131A22; --aws-darker:#0F1111; --aws-text:#E9ECEF; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#0F1111; color:var(--aws-text); font-family:'Segoe UI',Arial,sans-serif; padding:40px; }}
  .badge {{ display:inline-block; background:var(--aws-orange); color:#131A22; font-weight:700; font-size:12px; letter-spacing:1px; padding:6px 14px; border-radius:999px; text-transform:uppercase; margin-bottom:18px; }}
  h1 {{ font-size:26px; margin-bottom:6px; }}
  h1 span {{ color:var(--aws-orange); }}
  .subtitle {{ color:#9AA5B1; margin-bottom:24px; font-size:14px; }}
  form {{ margin-bottom:24px; }}
  input[type=file] {{ color:#E9ECEF; }}
  button {{ background:var(--aws-orange); color:#131A22; font-weight:700; border:none; padding:10px 18px; border-radius:8px; cursor:pointer; margin-left:10px; }}
  table {{ width:100%; border-collapse:collapse; background:var(--aws-dark); border:1px solid #2b3542; border-radius:8px; overflow:hidden; }}
  th, td {{ padding:10px 14px; text-align:left; border-bottom:1px solid #2b3542; font-size:14px; }}
  th {{ background:#1B2430; color:var(--aws-orange); text-transform:uppercase; font-size:12px; letter-spacing:1px; }}
</style>
</head>
<body>
  <span class="badge">Store-Ops Photo Uploader</span>
  <h1>NorthStar<span> Retail</span> — Shelf Photos</h1>
  <p class="subtitle">{count} photo(s) stored in s3://{bucket}/{prefix} via the VPC Gateway Endpoint</p>
  <form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="photo" required>
    <button type="submit">Upload</button>
  </form>
  <table>
    <tr><th>File</th><th>Size</th><th>Uploaded</th></tr>
    {rows}
  </table>
</body>
</html>"""


@app.route('/')
def index():
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
    objs = resp.get('Contents', [])
    rows = ''.join(
        "<tr><td>{}</td><td>{} bytes</td><td>{}</td></tr>".format(
            o['Key'].replace(PREFIX, ''), o['Size'], o['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
        )
        for o in objs
    )
    return PAGE.format(
        count=len(objs), bucket=BUCKET, prefix=PREFIX,
        rows=rows or '<tr><td colspan="3">No photos uploaded yet.</td></tr>'
    )


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['photo']
    key = PREFIX + f.filename
    s3.upload_fileobj(f, BUCKET, key)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
