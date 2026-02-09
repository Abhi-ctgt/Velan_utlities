#include "import_utils.hxx"

int ITK_user_main(int argc, char* argv[])

{

	int iStatus = ITK_ok;
	char* uname = ITK_ask_cli_argument("-u=");
	char* pass = ITK_ask_cli_argument("-p=");
	char* passfile = ITK_ask_cli_argument("-pf=");
	char* grp = ITK_ask_cli_argument("-g=");
	char* cpFilePath = ITK_ask_cli_argument("-file=");

	string strFilePath = (cpFilePath != NULL) ? string(cpFilePath) : "";
	
	if (argc == 5)
	{
		// Validate that all required command-line arguments are provided:
		// - uname: Username
		// - pass: Password
		// - grp:  Group
		
		if (uname != NULL && ( pass != NULL or passfile != NULL) && grp != NULL && !strFilePath.empty())

		{
			// Initialize the Teamcenter ITK (Integration Toolkit) session using the provided username (uname), password (pass), and group (grp).
			// If the return value equals ITK_ok, the initialization succeeded and the session is active.
			// Otherwise, the session failed to start
			// if ((iStatus = ITK_init_module(uname, pass, grp)) == ITK_ok)
			if ((iStatus = ITK_auto_login()) == ITK_ok)
			{
				
				std::cout << " ******************************************" << std::endl;
				std::cout << "           TC Login Successful             " << std::endl;
				std::cout << " ******************************************\n\n" << std::endl;
				
				vector<string> vDatasetNames = getDatasetNames(strFilePath);

				//cout << "\n\nExtracted Dataset Names: "; printVector(vDatasetNames);

				purgeDatasets(vDatasetNames);
							
				cout<<"\n\nPurge Complete...\n\n";
				logoutFromTeamcenter();
			}
			else
			{
				char* error = NULL;

				EMH_ask_error_text(iStatus, &error);

				cout<<"\nUnable to login to TC, ITK_auto_login() failed! ERROR: " << error;
				
				SAFE_SM_FREE(error);
			}

		}
		else
		{
			cout << "\n ";
			cout<<"\nInvalid arguments. Required Argument -u=\"< user >\" (-p=\"< password >\" | -pf=\"< password_file_path >\") -g=\"< group >\" -file=\"< file_path >\"";

		}
	}
	else
	{
		cout<<"\n command line argument mismatch..";
	}

	return iStatus;

	
}

// Utility to trim spaces from both ends of a string
static inline string trim(const string& s) {
	size_t start = s.find_first_not_of(" \t\r\n");
	size_t end = s.find_last_not_of(" \t\r\n");
	return (start == std::string::npos) ? "" : s.substr(start, end - start + 1);
}

vector<string> getDatasetNames(const string& strFilePath) {
	vector<string> vDatasetNames;
	ifstream file(strFilePath);
	if (!file.is_open()) {
		cout << "Error opening file: " << strFilePath << endl;
		return vDatasetNames;
	}
	string line;
	while (getline(file, line)) {
		if (line.empty())
			continue;
		stringstream ss(trim(line));
		string firstPart;

		if (getline(ss, firstPart, ','))   // read text before comma
		{
			firstPart = trim(firstPart);
			if (!firstPart.empty())
				vDatasetNames.push_back(firstPart);
		}
	}
	file.close();
	return vDatasetNames;
}

void printVector(vector<string>& objects) {

	for (auto str : objects) {
		cout << str << endl;
	}
	cout << endl;
}

void logoutFromTeamcenter() {
	int iStat = 0;
	iStat = ITK_exit_module(true);
	if (iStat != ITK_ok) {
		cout << "\n\nError logging-out from TC: " << iStat << endl;
		return;
	}
	cout << endl;
	std::cout << " ******************************************" << std::endl;
	std::cout << "          TC Logout Successful            " << std::endl;
	std::cout << " ******************************************\n\n" << std::endl;
}

/**
 * \brief Locates StyleSheet by type and name
 *
 * @param cls name of class of objects to search for. Subclasses are found, too
 * @param name name to look for (compared to object_name)
 */
std::vector<tag_t> findStyleSheet(const std::string& cls, const std::string& name) {
	int n = 0;
	tag_t* dsTags;
	tag_t searchClass = NULLTAG;
	std::vector<tag_t> result;

	POM_class_id_of_class(cls.c_str(), &searchClass);

	AE_find_all_datasets2(name.c_str(), &n, &dsTags);
	for (int i = 0; i < n; i++) {
		AE_purge_dataset_revs(dsTags[i]);
	}

	AE_find_all_datasets2(name.c_str(), &n, &dsTags);
	//std::cout << "\nFound " << n << " datasets with name <" << name << ">" << std::endl;
	for (int i = 0; i < n; i++) {
		char* uid;
		POM_tag_to_uid(dsTags[i], &uid);

		tag_t clsId = NULLTAG;
		POM_class_of_instance(dsTags[i], &clsId);

		logical clsHit = false;
		POM_is_descendant(searchClass, clsId, &clsHit);

		if (clsHit) {
			result.push_back(dsTags[i]);
		}
		else {
			char* objType;
			AOM_ask_value_string(dsTags[i], "object_type", &objType);
			if (cls == objType)
				result.push_back(dsTags[i]);
		}
	}

	SAFE_SM_FREE(dsTags);

	return result;
}

void purgeDatasets(vector<string>& vDatasetNames) {

	for (const auto strDatasetName : vDatasetNames) {
		auto vProcessedDatasets = findStyleSheet("Dataset", strDatasetName);
		//cout << "\nStylesheets found and purged with name <" << strDatasetName << ">: " << vProcessedDatasets.size() << std::endl;
	}
}