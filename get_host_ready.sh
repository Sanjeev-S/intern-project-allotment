scp -o StrictHostKeyChecking=no -r api/ requirements.txt sanjeev.s@10.32.58.130:/home/sanjeev.s
pssh -O StrictHostKeyChecking=no --host 10.32.58.130 'sudo apt-get install --yes python-pip'
pssh -O StrictHostKeyChecking=no --host 10.32.58.130 'sudo pip install -i http://10.85.59.116/artifactory/v1.0/artifacts/pypi -r requirements.txt'

