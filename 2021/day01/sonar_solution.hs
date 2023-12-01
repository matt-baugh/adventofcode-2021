import System.IO

readInt :: String -> Int
readInt = read

realData = do
        allSonarContents <- readFile "sonar_data.txt"
        return $ countIncreases $ map readInt $ filter (not . null) $ lines allSonarContents

testData :: [Int]
testData = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

countIncreases :: [Int] -> Int
countIncreases xs = sum $ map numberIncreases sumComparisons
  where
    triplets       = zip3 xs (tail xs) $ tail $ tail xs
    tripletSums    = map (\(x, y, z) -> x + y + z) triplets
    sumComparisons = zip tripletSums $ tail tripletSums

numberIncreases :: (Int, Int) -> Int
numberIncreases (a, b)
 | b > a     = 1
 | otherwise = 0

