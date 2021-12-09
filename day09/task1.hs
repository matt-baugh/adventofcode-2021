import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [[Int]]
convert xs
  = map (map (\c -> ord c - (ord '0'))) $ lines xs



splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [[Int]] -> Int -- [(Int, Int)]
solve xs
  = foldl1 (*) $ take 3 $ reverse $ sort basinSizes
  where
    h          = length xs
    w          = length (xs !! 0)
    allIndices = concatMap (\(i, js) -> map (\j -> (i, j)) js) $ zip [0..h-1] (replicate h [0..w-1])
    minIndices = map (\(i, j) -> [i, j]) $ filter isMin allIndices
    basinSizes = map (flip calcBasinSize xs) minIndices
    isMin :: (Int, Int) -> Bool
    isMin (i, j)
      = foldl (\acc nP -> acc && curP < nP) True adjPs
       where
         curP    = (xs !! i) !! j
         adjInds = adjacentIndices i j h w
         adjPs   = map (\[k, l] -> ((xs !! k) !! l)) adjInds


calcBasinSize :: [Int] -> [[Int]] -> Int
calcBasinSize [minI, minJ] xs
  = length $ calcBasinSize' [initMin] [initMin]
  where
    h       = length xs
    w       = length (xs !! 0)
    initMin = [minI, minJ]
    calcBasinSize' :: [[Int]] -> [[Int]] -> [[Int]]
    calcBasinSize' [] bs
      = bs
    calcBasinSize' front inBasin
      = calcBasinSize' newInds (newInds ++ inBasin)
      where
        nextInds  = concatMap (\p@[i, j] -> map (\nI -> (p, nI)) $ adjacentIndices i j h w) front
        validInds = filter (\(_, np) -> notElem np inBasin) nextInds
        lowerInds = filter (\([i1, j1], [i2, j2]) -> (xs !! i1) !! j1 <= ((xs !! i2) !! j2)) validInds
        newInds   = nub $ filter (\[i, j] -> (xs !! i) !! j /= 9) $ map snd lowerInds



adjacentIndices :: Int -> Int -> Int -> Int -> [[Int]]
adjacentIndices i j h w
  = adjInd i j w ++ (map reverse $ adjInd j i h)
  where
    adjInd :: Int -> Int -> Int -> [[Int]]
    adjInd f v max
      | v == 0       = [below]
      | v == max - 1 = [above]
      | otherwise    = [above, below]
      where
        above = [f, v - 1]
        below = [f, v + 1]


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
testInput = unlines [
 "2199943210",
 "3987894921",
 "9856789892",
 "8767896789",
 "9899965678"] 

testData = convert testInput
