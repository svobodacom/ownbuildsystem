#include <nlohmann/json.hpp>
#include <gtest/gtest.h>
#include <iostream>
#include "math.h"

TEST(Math, MaxShouldBeCalculated)
{
    ASSERT_TRUE(std::max(19, 1) == 19);
}


int main(int argc, char **argv)
{
	const auto json = nlohmann::json::parse("{}");

	testing::InitGoogleTest(&argc, argv);
   const auto status = RUN_ALL_TESTS();
   std::cin.get();


	return status;
}