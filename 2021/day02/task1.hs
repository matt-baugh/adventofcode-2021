import System.IO

readInt :: String -> Int
readInt = read

realResult = do
        allDiveContents <- readFile "dive_data.txt"
        return $ (solve . convert) allDiveContents

convertSecond :: [String] -> (String, Int)
convertSecond (a:b:[])
  =  (a, read b)

convert :: String -> [(String, Int)]
convert xs
  = map (convertSecond . words) $ lines xs

testData :: [(String, Int)]
testData = [
  ("forward", 5),                                                                     
  ("down", 5),                                                                        
  ("forward", 8),                                                                    
  ("up", 3),                                                                          
  ("down", 8),                                                                        
  ("forward", 2)]

solve :: [(String, Int)] -> Int
solve xs
  = h * d
  where
    (h, d) = accDistance xs

accDistance :: [(String, Int)] -> (Int, Int)
accDistance xs
  = foldl accDistance' (0, 0) xs
  where
    accDistance' (h, d) (code, dist)
      | code == "forward" = (h + dist, d)
      | code == "down"    = (h, d + dist)
      | code == "up"      = (h, d - dist)

