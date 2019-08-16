'''
    dropboxUploader
    
    Uploads a timelapse file to Dropbox
    If upload was successfull returns True
'''
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

def upload(self):

    errorMessages ={'noToken' : 'No Dropbox API Token Defined! Cannot Upload Timelapse %s!' % self.file_name ,
                    'invalidToken' : 'Invalid Dropbox API Token! Cannot Upload Timelapse %s!' % self.file_name,
                    'insufficientSpace' : 'Insufficient space on Dropbox! Cannot Upload Timelapse %s!' % self.file_name
                    }

    if self.api_token:
        db = dropbox.Dropbox(self.api_token)
    else:
        self._logger.info(errorMessages['noToken'])
        return

    try:
        db.users_get_current_account()
    except AuthError:
        self._logger.info(errorMessages['invalidToken'])

    with open(self.path, 'rb') as f:
        self._logger.info('Uploading %s to Dropbox...' % self.file_name)
        try:
            db.files_upload(f.read(), '/'+self.file_name, mode=WriteMode('overwrite'))
            self._logger.info('Uploaded %s to Dropbox!' % self.file_name)
            return True
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().error.is_insufficient_space():
                self._logger.info(errorMessages['insufficientSpace'])
            elif e.user_message_text:
                self._logger.info(e.user_message_text)
            else:
                self._logger.info(e)