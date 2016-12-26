CREATE TYPE RPSL_OBJECT_TYPE AS ENUM ('as-set', 'as-number');

--
-- List of rpsl_objects entities to expand
--
CREATE TABLE prefix_list_rpsl_object (
	rpsl_object_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	entity TEXT NOT NULL,				-- The name of the entity to expand
	entity_type RPSL_OBJECT_TYPE NOT NULL,		-- The type of the entity (as-set or as-number)
	registry TEXT[] NOT NULL,			-- A list of registries to pull data from when expanding the entity
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for when the row was created
	fetched TIMESTAMP,				-- A timestamp for when the entity was last fetched
	metadata JSONB NOT NULL DEFAULT '{}',		-- Addidional metadata for the entry, useful when integrating with other systems

	PRIMARY KEY (rpsl_object_id)
);

--
-- List of available versions of the rpsl_objects
--
CREATE TABLE prefix_list_version (
	version_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	rpsl_object_id INTEGER NOT NULL,		-- References the prefix_list_rpsl_object that has been expanded
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for when the row was created

	PRIMARY KEY (version_id),
	FOREIGN KEY (rpsl_object_id) REFERENCES prefix_list_rpsl_object (rpsl_object_id)
);

--
-- Versioned list of asns expanded from the rpsl_object
--
CREATE TABLE prefix_list_member_asn (
	member_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	version_id INTEGER NOT NULL,			-- References the version which in turn references the rpsl_object
	asn INTEGER NOT NULL,				-- Member ASN
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for then the row was created

	PRIMARY KEY (member_id),
	FOREIGN KEY (version_id) REFERENCES prefix_list_version (version_id)
);

--
-- Versioned list of prefixes expanded from the rpsl_object
--
CREATE TABLE prefix_list_member_prefix (
	member_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	version_id INTEGER NOT NULL,			-- References the version which in turn references the rpsl_object
	prefix CIDR NOT NULL,				-- Member prefix
	origin INTEGER NOT NULL,			-- Origin ASN
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for when the row was created

	PRIMARY KEY (member_id),
	FOREIGN KEY (version_id) REFERENCES prefix_list_version (version_id)
);

--
-- Local policy for asns expanded from the rpsl_object
--
CREATE TABLE prefix_list_member_asn_policy (
	policy_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	rpsl_object_id INTEGER NOT NULL,		-- References the rpsl_object
	asn INTEGER NOT NULL,				-- Member ASN
	permit BOOLEAN NOT NULL,			-- Wether or not the referenced ASN is permitted by local policy
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for when the row was created

	PRIMARY KEY (policy_id),
	FOREIGN KEY (rpsl_object_id) REFERENCES prefix_list_rpsl_object (rpsl_object_id)
);

--
-- Local policy for prefixes expanded from the rpsl_object
--
CREATE TABLE prefix_list_member_prefix_policy (
	policy_id SERIAL NOT NULL,			-- Auto-incrementing unique key
	rpsl_object_id INTEGER NOT NULL,		-- References the rpsl_object
	prefix CIDR NOT NULL,				-- Member prefix
	permit BOOLEAN NOT NULL,			-- Wether or not the referenced prefix is permitted by local policy
	created TIMESTAMP NOT NULL DEFAULT NOW(),	-- A timestamp for when the row was created

	PRIMARY KEY (policy_id),
	FOREIGN KEY (rpsl_object_id) REFERENCES prefix_list_rpsl_object (rpsl_object_id)
);
