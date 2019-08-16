'''
    dropboxUploader
    Uploads a timelapse file to dropbox
    if upload was successfull returns true
'''
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

def upload(self):
    if self.api_token:
        db = dropbox.Dropbox(self.api_token)
    else:
        self._logger.info('No Dropbox API Token Defined! Cannot Upload Timelapse %s!' % self.file_name)
        return

    try:
        db.users_get_current_account()
    except AuthError:
        self._logger.info('Invalid Dropbox API Token! Cannot Upload Timelapse %s!' % self.file_name)

    with open(self.path, 'rb') as f:
        self._logger.info('Uploading %s to Dropbox...' % self.file_name)
        try:
            db.files_upload(f.read(), '/'+self.file_name, mode=WriteMode('overwrite'))
            self._logger.info('Uploaded %s to Dropbox!' % self.file_name)
            return True
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().error.is_insufficient_space():
                self._logger.info('Insufficient space on Dropbox! Cannot Upload Timelapse %s!' % self.file_name)
            elif e.user_message_text:
                self._logger.info(e.user_message_text)
            else:
                self._logger.info(e)