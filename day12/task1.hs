import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [(String, [String])]
convert xs
  = map (\x -> (x, lookupAll x nsCons)) caves
  where
    initCons = map (splitOn '-') $ lines xs
    caves    = nub $ concat initCons
    allCons  = concatMap (\c -> map (\[x, y] -> (x, y)) [c, reverse c]) initCons
    nsCons   = filter (\p -> snd p /= "start") allCons



splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain


lookupAll :: (Eq a) => a -> [(a, b)] -> [b]
lookupAll x xs
  = map snd $ filter (\p -> x == fst p) xs


solve :: [(String, [String])] -> Int
solve ts
  = length $ explore "start" [] False ts


explore :: String -> [String] -> Bool -> [(String, [String])] -> [[String]]
explore "end" _ _ _
  = [["end"]]
explore curr visited hasRep ts
  | hasRep    = nrsRes
  | otherwise = nrsRes ++ rsRes
  where
    (nrs, rs)  = partition (flip notElem visited) $ fromJust $ lookup curr ts
    vs         = if all isLower curr then (curr : visited) else visited
    nrsRes     = concatMap (\n -> map (curr:) $ explore n vs hasRep ts) nrs
    rsRes      = concatMap (\n -> map (curr:) $ explore n vs True ts) rs



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



testInput1 :: String
testInput1 = unlines [
 "start-A",
 "start-b",
 "A-c",
 "A-b",
 "b-d",
 "A-end",
 "b-end"]

testInput2 :: String
testInput2 = unlines ["dc-end",
 "HN-start",
 "start-kj",
 "dc-start",
 "dc-HN",
 "LN-dc",
 "HN-end",
 "kj-sa",
 "kj-HN",
 "kj-dc"]

testInput3 :: String
testInput3 = unlines ["fs-end",
 "he-DX",
 "fs-he",
 "start-DX",
 "pj-DX",
 "end-zg",
 "zg-sl",
 "zg-pj",
 "pj-he",
 "RW-he",
 "fs-DX",
 "pj-RW",
 "zg-RW",
 "start-pj",
 "he-WI",
 "zg-he",
 "pj-fs",
 "start-RW"]


testData1 = convert testInput1
testData2 = convert testInput2
testData3 = convert testInput3
