virtualenv -p python3 venv
source venv/bin/activate
pip3 install psycopg2-binary
pip3 install requests

drop
	table
		chunks;

create
	table
		chunks ( id serial primary key,
		file_name varchar,
		abs_path varchar,
		transcription varchar,
		url varchar,
		created_at timestamp,
		updated_at timestamp,
		file_size int,
		is_verified boolean )
