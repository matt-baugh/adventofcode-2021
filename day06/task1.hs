import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [Int]
convert xs
  = map read $ splitOn ',' xs


splitOn :: Char -> String -> [String]
splitOn _ "" = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [Int] -> Int
solve xs
  = sum $ breedFish (countFish xs) 256


breedFish :: [Int] -> Int -> [Int]
breedFish xs@(y:ys) i
  | i == 0    = xs
  | otherwise = breedFish ((addToElem ys 6 y) ++ [y]) $ i - 1


countFish :: [Int] -> [Int]
countFish xs
  = foldl (\cs i-> addToElem cs i 1) initCounts xs
  where
    initCounts = replicate 9 0


splitBetween :: Int -> Int -> [a] -> ([a], [a], [a])
splitBetween i1 i2 xs
  = (first, second, third)
  where
    (first, remaining) = splitAt i1 xs
    (second, third)    = splitAt (i2 - i1 + 1) remaining


addToElem :: [Int] -> Int -> Int -> [Int]
addToElem xs i c 
  = xs' ++ ((x + c) : xs'')              
  where                                  
    (xs', x:xs'') = splitAt i xs

testInput :: String
testInput = "3,4,3,1,2" 

testData = convert testInput
