import os.path
from nextgisweb_filebucket.file_bucket import command
from nextgisweb_filebucket.file_bucket.model import (
    FileBucket,
    FileBucketFile,
)

import pytest
import transaction

TEST_FILE = {"name": "mie_phyle.txt", "content": "test content".encode("utf-8")}


@pytest.mark.skip('Legacy model')
def test_migrate_file_storage(ngw_env, ngw_webtest_app):
    webapp = ngw_webtest_app
    webapp.authorization = ("Basic", ("administrator", "admin"))

    # Make legacy file_bucket
    data = {
        "resource": {"cls": "file_bucket", "display_name": "test-legacy-bucket", "parent": {"id": 0}},
        "file_bucket": {"files": []}
    }
    resp = webapp.post_json("/api/resource/", data)
    bucket_id = resp.json["id"]

    fb = FileBucket.filter_by(id=bucket_id).one()
    fb.stuuid = "aa" + "bb" + "legacy_bucket_dir"

    legacy_dir = ngw_env.file_bucket.dirname(fb.stuuid, makedirs=True)

    srcfile = os.path.abspath(os.path.join(legacy_dir, TEST_FILE["name"]))
    with open(srcfile, "wb") as f:
        f.write(TEST_FILE["content"])

    fbf = FileBucketFile(name=TEST_FILE["name"], size=1, mime_type="no_matter")

    fb.files.append(fbf)
    transaction.commit()

    # Run migrate command
    cmd = command.MigrateFileStorageCommand()
    cmd.execute(args="", env=ngw_env)

    # Check
    fb = FileBucket.filter_by(id=bucket_id).one()
    assert fb.stuuid == None
    fbf = fb.files[0]
    assert fbf.fileobj

    dstfile = ngw_env.file_storage.filename(fbf.fileobj)
    with open(dstfile, "rb") as f:
        assert f.read() == TEST_FILE["content"]

    webapp.delete("/api/resource/%d" % bucket_id)
