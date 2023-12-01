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



solve :: [[Int]] -> Int
solve xs
  = fst $ stepOctopi xs 100


stepOctopi :: [[Int]] -> Int -> (Int, [[Int]])
stepOctopi os 0
  = (0, os)
stepOctopi os n
  = (numFlash + nF, os'')
  where
    allInds    = getAllInds os
    flashedOs  = flashAdj (map (map (1+)) os) [] allInds
    numFlash   = sum $ map (length . filter (> 9)) flashedOs
    os'        = map (map (\f -> if f > 9 then 0 else f)) flashedOs
    (nF, os'') = stepOctopi os' (n-1)


flashAdj :: [[Int]] -> [(Int, Int)] -> [(Int, Int)] -> [[Int]]
flashAdj os done rem
  | new == [] = os
  | otherwise = flashAdj os' (done ++ new) rem'
  where
    (new, rem') = partition (\p@(i, j) -> (os !! i) !! j > 9) rem
    h           = length os
    w           = length (os !! 0)
    toUpdate    = concatMap (\(i, j) -> adjacentIndices i j h w) new
    newRowIs   = nub $ map fst toUpdate
    os'         = map updateRow $ zip os [0..]
    rowToCols   = map (\i -> (i, map snd (filter (\p -> fst p == i) toUpdate))) newRowIs
    updateRow :: ([Int], Int) -> [Int]
    updateRow (xs, i)
      | elem i newRowIs = map (\(f, j) -> f + countIn j (fromJust $ lookup i rowToCols)) $ zip xs [0..]
      | otherwise       = xs 



countIn :: Eq a => a -> [a] -> Int
countIn x
  = length . filter (==x)

    
getAllInds :: [[a]] -> [(Int, Int)]
getAllInds xs
  = concatMap (\(i, js) -> map (\j -> (i, j)) js) $ zip [0..h-1] $ replicate h [0..w-1]
  where
    h = length xs
    w = length (xs !! 0)

adjacentIndices :: Int -> Int -> Int -> Int -> [(Int, Int)]
adjacentIndices i j h w
  = map (\[f, s] -> (f, s)) $ adjInd i j w ++ (map reverse $ adjInd j i h) ++ validDiag
  where
    adjInd :: Int -> Int -> Int -> [[Int]]
    adjInd f v max
      | v == 0       = [below]
      | v == max - 1 = [above]
      | otherwise    = [above, below]
      where
        above = [f, v - 1]
        below = [f, v + 1]
    adjDiag = concatMap (\[k, l] -> map (\d -> [k + d, l]) [-1, 1])
                        $ map (\d -> [i, j + d]) [-1, 1]
    validDiag = filter (\[k, l] -> 0 <= k && k < h && 0 <= l && l < w) adjDiag


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
 "5483143223",
 "2745854711",
 "5264556173",
 "6141336146",
 "6357385478",
 "4167524645",
 "2176841721",
 "6882881134",
 "4846848554",
 "5283751526"]

testData = convert testInput
