import System.IO
import Data.List
import Data.Bits
import Data.Char

realResult = do
        allDiveContents <- readFile "data.txt"
        return $ (solve . convert) allDiveContents

convertSecond :: [String] -> (String, Int)
convertSecond (a:b:[])
  =  (a, read b)

convert :: String -> [String]
convert xs
  = lines xs

testData :: [String]
testData = [ "00100", "11110","10110","10111","10101","01111","00111","11100","10000","11001","00010","01010"]

solve :: [String] -> Int
solve xs
  = gamma * epsilon
  where
    gammaStr   = filterMostCommon xs 0
    gamma      = toBinaryNum gammaStr
    epsilonStr = filterLeastCommon xs 0
    epsilon    = toBinaryNum epsilonStr
    
invertStr :: String -> String
invertStr "" = ""
invertStr (c:ss)
  | c == '0' = '1' : invertStr ss
  | c == '1' = '0' : invertStr ss 


toBinaryNum :: String -> Int
toBinaryNum s
  = foldl (\acc c -> acc * 2 + ord c - ord '0') 0 s

filterMostCommon :: [String] -> Int -> String
filterMostCommon [s] _ = s
filterMostCommon xs i
  = filterMostCommon (filter (\s -> s !! i == mc) xs) $ i + 1
  where
    bits = transpose xs
    mc   = getMostCommon (bits !! i) 0 0

filterLeastCommon :: [String] -> Int -> String
filterLeastCommon [s] _ = s
filterLeastCommon xs i
  = filterLeastCommon (filter (\s -> s !! i == lc) xs) $ i + 1
  where
    bits = transpose xs
    mc   = getMostCommon (bits !! i) 0 0
    lc   = if mc == '1' then '0' else '1'

getMostCommon :: String -> Int -> Int -> Char
getMostCommon "" zeros ones
  | zeros > ones = '0'
  | otherwise    = '1'
getMostCommon (c:ss) zeros ones
  | c == '0' = getMostCommon ss (zeros + 1) ones
  | c == '1' = getMostCommon ss zeros $ ones + 1 
