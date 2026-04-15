PRAGMA foreign_keys = ON;

INSERT INTO category (categoryId, categoryName, categoryImage) VALUES
(1, 'Biographies', 'biographies-category.jpg'),
(2, 'Learn to Play', 'learn-to-play-category.jpg'),
(3, 'Music Theory', 'music-theory-category.jpg'),
(4, 'Scores and Collections', 'scores-and-collections-category.jpg');

INSERT INTO book (bookId, categoryId, title, author, isbn, price, image, readNow) VALUES
(1, 1, 'Beethoven: Anguish and Triumph', 'Jan Swafford', '9780618054749', 24.99, 'beethoven.gif', 1),
(2, 1, 'Lady Gaga: Applause', 'Annie Zaleski', '9781250203564', 19.99, 'madonna.jpg', 0),
(3, 1, 'Duke: A Life of Duke Ellington', 'Terry Teachout', '9781594036682', 21.99, 'ellington.jpg', 0),
(4, 1, 'Clapton: The Autobiography', 'Eric Clapton', '9780767920551', 18.99, 'clapton.jpg', 0),
(5, 2, 'Hal Leonard Guitar Method Book 1', 'Will Schmid', '9780793523054', 14.99, 'guitar.jpg', 1),
(6, 2, 'Alfred''s Basic Adult Piano Course Lesson Book 1', 'Willard A. Palmer', '9780882846163', 16.99, 'piano.jpg', 1),
(7, 3, 'Music Theory for Dummies', 'Michael Pilhofer', '9781119575528', 22.99, 'theory.jpg', 1),
(8, 4, 'The Real Book: Volume I (C Edition)', 'Hal Leonard Corp.', '9780634060380', 39.99, 'scores.jpg', 0),

(9, 2, 'Ukulele for Dummies', 'Alistair Wood', '9781119731900', 17.99, 'ukulele.jpg', 0),
(10, 2, 'Essential Elements for Band - Flute Book 1', 'Tim Lautzenheiser', '9780634003202', 12.99, 'flute-book.jpg', 0),
(11, 3, 'Tonal Harmony', 'Stefan Kostka', '9781259447099', 34.99, 'tonal-harmony.jpg', 0),
(12, 4, 'Bach: The Well-Tempered Clavier', 'Johann Sebastian Bach', '9780739003275', 27.99, 'bach-wtc.jpg', 1),
(13, 4, 'The Complete Beatles Songs', 'Hal Leonard Corp.', '9781458499547', 29.99, 'beatles-songs.jpg', 0),
(14, 3, 'Contemporary Musicianship: Analysis and the Artist', 'Jennifer Snodgrass', '9780199990870', 118.12, 'cont-muc.jpg', 0);
