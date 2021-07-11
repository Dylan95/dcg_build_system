//a precompiled header that is meant to be used specifically for s0.cpp
#include "s0_pch.hpp"

//this was already included in the precompiled header.
//including it again won't cause any problem.  the include gaurd will have already
//been defined, so including it again will have no effect whatsoever.
#include <vector>

using namespace std;

int main(){
	vector<int> v;
	return 0;
}


