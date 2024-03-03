import yadisk
import os
import shutil


class Disk:
    def __init__(self, name_folder, root_dir, tokens=()):
        self.tokens = tokens
        self.disk_root_dir = 'MasterThesisExperiments1'
        self.name_folder = name_folder
        self.experiment_path = os.path.join(self.disk_root_dir, self.name_folder)
        self.root_dir = root_dir
        self.__init_yadisk()

    def __init_yadisk(self):
        self.disk = yadisk.YaDisk(*self.tokens)
        exist_folder = False
        for folder in self.disk.listdir(self.disk_root_dir):
            if folder['name'] == self.name_folder:
                exist_folder = True

        if not exist_folder:
            self.disk.mkdir(os.path.join(self.experiment_path))
            self.disk.mkdir(os.path.join(self.experiment_path, 'saves'))
            self.disk.mkdir(os.path.join(self.experiment_path, 'metrics'))

    def download_saves(self, name_save):
        if not os.path.exists(os.path.join(self.root_dir, 'saves')):
            os.mkdir(os.path.join(self.root_dir, 'saves'))
        self.disk.download(os.path.join(self.experiment_path, 'saves', name_save),
                           os.path.join(self.root_dir, 'saves', name_save))

    def download_logs(self, log_dir):
        _, file = os.path.split(log_dir)
        if self.disk.exists(os.path.join(self.experiment_path, 'metrics', file + '.zip')):
            self.disk.download(os.path.join(self.experiment_path, 'metrics', file + '.zip'),
                               os.path.join(self.root_dir, 'logs', file + '.zip'))
            shutil.unpack_archive(os.path.join(self.root_dir, 'logs', file + '.zip'),
                                  os.path.join(self.root_dir, 'logs', file), 'zip')
            os.remove(os.path.join(self.root_dir, 'logs', file + '.zip'))

    def upload(self, path, folder_for_save):
        _, file = os.path.split(path)
        if os.path.isdir(path):
            shutil.make_archive(path, 'zip', path)
            self.disk.upload(path + '.zip', os.path.join(self.experiment_path, folder_for_save, file + '.zip'),
                             overwrite=True)
            os.remove(path + '.zip')
        else:
            self.disk.upload(path, os.path.join(self.experiment_path, folder_for_save, file),
                             overwrite=True)


if __name__ == '__main__':
    disk = Disk('exp1', '/Users/andrejcvanov/PycharmProjects/master_thesis/utils/scripts')
    disk.upload('/Users/andrejcvanov/PycharmProjects/master_thesis/utils/scripts', 'saves')
