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


splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [Int] -> Int
solve xs
  = foldl (\m x -> min m $ calcCost xs x) (calcCost xs mn) [mn+1..mx]
  where
    mn = minimum xs
    mx = maximum xs 


calcCost :: [Int] -> Int -> Int
calcCost xs x
  = sum $ map (cumSum . abs . (x-)) xs
  where
    cumSum :: Int -> Int
    cumSum y
      = y * (y + 1) `div` 2
  


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
testInput = "16,1,2,0,4,2,7,1,2,14" 

testData = convert testInput
