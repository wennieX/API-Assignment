
CREATE TABLE information (
	"id"  			    INTEGER NOT NULL PRIMARY KEY,
	"first_name"        VARCHAR(255),
	"last_name"			VARCHAR(255),
	"email"             VARCHAR(255),
	"gender"			VARCHAR(64),
	"ip_address"        VARCHAR(64),
	"country_code"	    VARCHAR(64)
);

-- Test examples
-- INSERT INTO information (id,first_name,last_name,email,gender,ip_address, country_code) VALUES 
-- (1, 'Paul', 'Walker', 'paul.walker@gmail.com', 'male','192.168.0.2','US');

