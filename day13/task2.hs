import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> ([(Int, Int)], [(Char, Int)])
convert xs
  = (map readCoord cs, zip fAxes fCs) 
  where
    [cs, fs] = splitOn [] $ lines xs
    fIs      = zip fs $ map (fromJust . (elemIndex '=')) fs
    fAxes    = map (\(f, i) -> f !! (i - 1)) fIs
    fCs      = map (\(f, i) -> read (drop (i + 1) f)) fIs


solve :: ([(Int, Int)], [(Char, Int)]) -> [[Char]]
solve (coords, folds)
  = map (\i -> map (\j -> if elem (j, i) finalCoords then '#' else '.') [0..maxX]) [0..maxY]
  where
    finalCoords = foldl foldPaper coords folds
    maxX        = maximum $ map fst finalCoords
    maxY        = maximum $ map snd finalCoords


foldPaper :: [(Int, Int)] -> (Char, Int) -> [(Int, Int)]
foldPaper coords (fc, fi)
  | fc == 'x' = nub $ map (\(x, y) -> (min x (2 * fi - x), y)) coords
  | fc == 'y' = nub $ map (\(x, y) -> (x, min y (2 * fi - y))) coords


readCoord :: String -> (Int, Int)
readCoord s
  = (read s1, read s2)
  where
    [s1, s2] = splitOn ',' s


splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain


lookupAll :: (Eq a) => a -> [(a, b)] -> [b]
lookupAll x xs
  = map snd $ filter (\p -> x == fst p) xs


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
testInput = unlines ["6,10",
 "0,14",          
 "9,10",          
 "0,3",           
 "10,4",          
 "4,11",          
 "6,0",           
 "6,12",          
 "4,1",           
 "0,13",          
 "10,12",         
 "3,4",           
 "3,0",           
 "8,4",           
 "1,10",          
 "2,14",          
 "8,10",          
 "9,0",           
 "",              
 "fold along y=7",
 "fold along x=5"] 

testData = convert testInput
