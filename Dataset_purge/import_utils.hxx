#pragma once

#include <tccore\tctype.h> 
#include <tcinit\tcinit.h>
#include <tccore\aom_prop.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <tccore/item.h>
#include <vector>
#include <string>
#include <cstdio>   
#include <cstdlib>
#include <algorithm>
#include <ae\dataset.h>
#include <tccore\aom.h>
#include <ae\datasettype.h>
#include <qry/rep.h>
#include <sa/tcfile.h>
#include <tc/emh.h>
#include <qry/crf.h>
#include <utility>
#include <user_exits\epm_toolkit_utils.h>

using namespace std;

void logoutFromTeamcenter();
void printVector(vector<string>& objects);
void purgeDatasets(vector<string>& vDatasetNames);
vector<string> getDatasetNames(const string& strFilePath);