import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

type Rules = [(Char, [(Char, Char)])]
type Mem = [(Int, Char, Char, [(Char, Int)])]

convert :: String -> (String, Rules)
convert xs
  = (str, map (\x -> (x, lookupAll x rules)) allChars) 
  where
    [[str], rs] = splitOn [] $ lines xs
    rules     = map (\r -> (r !! 0, (r !! 1, r !! 6))) rs
    allChars  = nub $ concatMap (\(a, (b, c)) -> [a, b, c]) rules

solve :: (String, Rules) -> Int
solve input
  = last allCounts - head allCounts
  where
    res       = expandAll input 40
    allCounts = sort $ map snd res
    

expandAll :: (String, Rules) -> Int -> [(Char, Int)]
expandAll (str, rs) i
  = combineCounts [(head str, 1)] $ foldl1 combineCounts $ map fst allRes
  where
    exPairs  = zip str $ tail str
    allRes   = scanl (\(_, mem) (a, b) -> memoExpand a b i rs mem)  ([], []) exPairs


expand :: Char -> Char -> Int -> Rules -> Mem -> ([(Char, Int)], Mem)
expand a b i rs mem
  | i == 1    = (makeCounts middle b, mem)
  | otherwise = (combineCounts c1 c2, m2)
  where
    middle   = jLookup b (jLookup a rs)
    (c1, m1) = memoExpand a middle (i - 1) rs mem
    (c2, m2) = memoExpand middle b (i - 1) rs m1
    makeCounts :: Char -> Char -> [(Char, Int)]
    makeCounts x y
      | x == y    = [(x, 2)]
      | otherwise = [(x, 1), (y, 1)]


combineCounts :: [(Char, Int)] -> [(Char, Int)] -> [(Char, Int)]
combineCounts cs cs'
  = map (\k -> (k, lookupOr k cs 0 + (lookupOr k cs' 0))) allKeys
  where
    allKeys = nub $ map fst cs ++ map fst cs'


memoExpand :: Char -> Char -> Int -> Rules -> Mem -> ([(Char, Int)], Mem)
memoExpand a b i rs mem
  | isNothing res = (res', (i, a, b, res') : m')
  | otherwise     = ((\(_, _, _, s) -> s) $ fromJust res, mem)
  where
    res        = find (\(i', a', b', _) -> a == a' && b == b' && i == i') mem
    (res', m') = expand a b i rs mem



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


lookupOr :: (Eq a) => a -> [(a, b)] -> b -> b
lookupOr x ps y
  = fromMaybe y $ lookup x ps


jLookup :: (Eq a) => a -> [(a, b)] -> b
jLookup x = (fromJust . lookup x)


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
testInput = unlines ["NNCB",
 "",
 "CH -> B",
 "HH -> N",
 "CB -> H",
 "NH -> C",
 "HB -> C",
 "HC -> B",
 "HN -> C",
 "NN -> C",
 "BH -> H",
 "NC -> B",
 "NB -> B",
 "BN -> B",
 "BB -> N",
 "BC -> B",
 "CC -> N",
 "CN -> C"]
testData = convert testInput
