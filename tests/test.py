"""Test SeededRGN."""
import hashlib

import pytest

from seedrandom import SeededRNG

hash_funcs = [
    hashlib.md5,
    hashlib.sha1,
    hashlib.sha224,
    hashlib.sha256,
    hashlib.sha384,
    hashlib.sha512,
    hashlib.blake2s,
    hashlib.blake2b,
]
payloads = [
    ([b"First", b"Second"], {}),
    ([b"Second", b"First"], {}),
    ([], {"ordered": [b"First_ord", b"Second_ord"]}),
    ([b"First", b"Second"], {"ordered": [b"First_ord", b"Second_ord"]}),
    ([b"Second", b"First"], {"ordered": [b"First_ord", b"Second_ord"]}),
]
prep_rng = SeededRNG(*payloads[3][0], **payloads[3][1], hash_func=hashlib.md5)


to_type = [None] * len(payloads)
to_type[0] = {
    bytes: {
        "openssl_md5": b"A]\xd7Q:\x83\x9c\xee\xbd\x8c1\xd9\xac\xb2\xae\xb4",
        "openssl_sha1": b"\x90\xb9$\xec\xfc8\xa7\xa6\xcf\xe3\x94c\xd7\xd3\xc4HG\xe0\x94\x91",
        "openssl_sha224": b"\xc0\xe2e\x10\xc4'\x07\r\x0f\xa6u]\x1d\xfd\x93u\x91\x85k\xa5b\xbb\x00CB\xabW3",
        "openssl_sha256": b"\x93\x0e\x81w\x1dj[\x15\xb5\xd2r\x80\x0bvY\x14\xe7\x95\xaa:\x99\xc3c\xad8\xaa7\xd9%zXa",
        "openssl_sha384": b"C\xeb\xf4L\x0bJ\x08*8\xc3\xbd\x15\xba\xb6\x17\x8aW8\x12O.L\xd8\xf9\xe0!\xe6\xd1\x83\x82\r\xf5\xa3\xa1\xd0\x04\xac\xaf\xf1X\xa2I\xb7\xa1u3\xf7:",
        "openssl_sha512": b"x;\xb2\xe6\x7fL\xf6\x98\x92cO\xf1\x08\xe6CRlg\x1bi/0\x8b\xe9\x1c\xa6?:\xeb\xb8\x1c\\H\xa7\x0b\xcdb\x82\xb7&3\x03%\xc3\x17n\x97k\xb8*\\U\xcfX\xd6A\xeb\xb0\x1d\x13\xbb\xe0^\x15",
        "blake2s": b"\xbb\xbb}N\xedK\xdf\x95h\xb7\xb1\xcc@\n\xb2pJZ\x17u\xa1\xd2&#\xbd\xe8B\xa2o`2\xf3",
        "blake2b": b"\xf1\xcaw\x8d*\xc5\xb5\xa7`\xb9\xc7\xaa\xb8\xe3\xb3N9\xces:\xb9mW\xd0D\xd1K\xc2\xb6u\x0f\x1a\x07\x0b\x8cB\x84\x8f\x12\x01\xea\x86\x1e\x04\xe3\x90\x06\xea:\x9d\xd8{+\x0b#)\x9c`\x90@z\x00\xfeq",
    },
    int: {
        "openssl_md5": 86887070487518460417915583009259695796,
        "openssl_sha1": 826223525544552817421607543562026585018935055505,
        "openssl_sha224": 20313093413837370023722829488895854712891113913869235402207721641779,
        "openssl_sha256": 66515618137257254541944130677363949898744545963502109205321952142485469419617,
        "openssl_sha384": 10454105873010625848360228491749326249464899333330221665113556235711632991608080292597075329193631108937103384508218,
        "openssl_sha512": 6297123566419662806357442127749586059464840707125988982525190136673166600317276870134828660351293760483040343357596469991821522236495917498413486788599317,
        "blake2s": 84913767932343786974604549124681371648632907095705268700612072653247261717235,
        "blake2b": 12663616282108173853033236834043144259608326848502997548064212449714738710044605373722031754948451584177031264214426208374456843146627159602570955709283953,
    },
}
to_type[1] = to_type[0]  # Outputs from 0 and 1 payloads have to be the same
to_type[2] = {
    bytes: {
        "openssl_md5": b"\xa7\xdb\xa3\xac\xb1\x89\x046E\x82\x90\xffm\x01\xc8\xcf",
        "openssl_sha1": b"E\xef\xaa\x90\xe6~\xc3S*\x16\x06\xf7!d\xa6<\x97\x1f\x8bG",
        "openssl_sha224": b">\xa2\x07\xa9\x04H\xce\x8fRP\xc9\xd6\x8e;\xfa\x16\x16\xd9\xf8\x11\xd3\x7fP\xbfA\x84\xb3N",
        "openssl_sha256": b"\xd0\xafJ\x83\xc1I\x1dkCEi\x8e7\xa4o\xe0\xd0h\xc7w\x9d\xcc'o\xab\xc6s\x9a\x06\xe4\xbf\xd8",
        "openssl_sha384": b'\x9b\xa3\xd4\xfe\x93"q\x1a\xb93\x16\x12+)S\xd9\x1f\xef\xcf\x1d\xa0i\xb2\x8f\n\x8b!0\xc2S\xd0\xa9\x16b\xba+\xff\x9fQ\x93\x8eJI7~E\xf7\n',
        "openssl_sha512": b"\xff\xaf\xe7\xe1_\xb3R[O[\xed\xeb\x12\xd8\x81gk.m\xeb\x1c5q\xf9)\xaf\xadL\xee\xf8+L\n\xbd\xf8R\xb1t\x8b\x05\x19\xc2\xad\xe1\xe2\xca\x81\x18\x83O\xe5h\x838\xef\x8a\xe1?b\x83\x9b`\xb3\x96",
        "blake2s": b'\xbb\x9a\xf3\xe3\x1d\xfcA\xcc\xc5\x93S\x9a\xec:\x9a\x08z\x88\x85\x99\xf7\xea\x91\xb6x\x00\xfb\x82"\xc2$K',
        "blake2b": b"wR\x07\xf5)\x86\x95G6\xba\xbaF\xca\xdf\xder\xdf\x16\x9e\xdbXV\x1a\xe5Xr\xeb\x99\xe7\x8avC\x01\x10@\xd0\x007R\xc7\x90>\xf6y\xca\xce\xc2\x82W\x18\x127\xaa1H\xfaw\x0f9T\xbd=\x1e\x8d",
    },
    int: {
        "openssl_md5": 223121508023053915167593245236862765263,
        "openssl_sha1": 399265099684943612053523868506304602181363272519,
        "openssl_sha224": 6596017327523610741023504543279554762464656161134617436376967459662,
        "openssl_sha256": 94390785022993651962487887495405183266459339476524463287719691378702246264792,
        "openssl_sha384": 23955183650612049185143126477410310778188329075889424285903678701309997455720551273155020137103383999576979223738122,
        "openssl_sha512": 13391421701272821393603640485300504071883816826531413055648909144818643814535822212998295950921452703111178763035507290455800978052021014498426299707601814,
        "blake2s": 84856280380474678344608588081910192497865490841532343476087781581609534366795,
        "blake2b": 6249318203807897128577037715090133374208263827583289499223024582027256491947635616704321057681928530052289739375171135751962581303065023891280534760660621,
    },
}
to_type[3] = {
    bytes: {
        "openssl_md5": b"\xd1\xac\x9bE\xbd\x80\x18\xab\xd7\x83\x1f^P\xe2\x02o",
        "openssl_sha1": b"\xa7\xeb\xbbZ\xefv\x8b(j:Ve\x8e\x17\x9e\x0f\xfcJ\xf9\xd0",
        "openssl_sha224": b"t\x7f\x18\x86A\x80N\x86<\x00p\r\xdd\xdd\x84\x0f\xd2\xde\xbe\x0b\x98\xc4:\xbe.\xacL\xd3",
        "openssl_sha256": b"\xef\xdf\xe3Y\xca\xf5,\xb5\xae\x9f6\x8eRY\x1aP\xf0q~Y\x9f\xb2\x1d@\xb7\x06:\xce\xd6w\x89\x8a",
        "openssl_sha384": b"=k\x08\xfe\xb6\xf0\x7f\xe6\xf0\xfc\xee\xea\xd1+s\x81\x08vf\xa0\xe3ai\xb5'\x1c\x87^|\xfbO2\xc6}\xeb\x12<ZT\x91\xbb7\xdd>5r\x06\xa4",
        "openssl_sha512": b"2\x13^\x10\x1eaw+\xe2\x18 c\x8e:\xc2+6\x8d\x7f\xabI\xc1>sl[\x98\x8a\xdd6\x19\xbdAp\xbf\xd2\x83FZg\x04\x92\x1f\xa6\x0b\xc8\xef\xb0f\xf3\xe5\x88U&\xa2A\x84\xce\xb0\x9c\x0e2\x93\xae",
        "blake2s": b"\xcaE\x7f\xb5n]\xf1\xacA[\x96\xef|\xa9\xf3\xfd\x08\xeb$\x0f\xa2\xd6w,\x88+\xd5\xd5\xaf\xc3v\xbd",
        "blake2b": b"\x90\x95\xcfQx\xf5\xc3q\xdf7\xddJ\xf9;\x92\x06\xdc\xcf]\x93\x8b\xf3\x97\x0f\x90\x85\xe0g?\tD\x86\xd0\xb9&\xd4\xf4\x0e\xad\x82\x9f\xd9\xdc\x12\xcf\xb1\xcf?\xfd\x11\xf6\xade]@Z\xb5\xbf \x19\xa6:&\xe0",
    },
    int: {
        "openssl_md5": 278704875477594713150020933174912221807,
        "openssl_sha1": 958658454790419163514619899931673406988532513232,
        "openssl_sha224": 12268510012498361412654661200852009401960591443117334603058591321299,
        "openssl_sha256": 108498346824076163278003793298698233103667735156409883038282803355917781272970,
        "openssl_sha384": 9453111692503021675010387228470520947003179483279393046340068838148644885860715683423502197630687488135284808353444,
        "openssl_sha512": 2622674809739354364080808784186685622193308335435911040647446072987193677168337363225414091033970878803371102165155387749999224291735444877476734128264110,
        "blake2s": 91489989274448906543851276317672555592408731098822456960024906460926358812349,
        "blake2b": 7572541092664580964992543329828237190870400002132158926611230644242968470991842770645022384814734512640083390228095993882313074751355245873869456867469024,
    },
}
to_type[4] = to_type[3]  # Outputs from 3 and 4 payloads have to be the same


@pytest.mark.parametrize("payload", payloads)
@pytest.mark.parametrize("hash_func", hash_funcs)
@pytest.mark.parametrize("dtype", [bytes, int])
def test_to_type(dtype, hash_func, payload):
    """Test converting RNG to int and bytes."""
    payload_id = payloads.index(payload)
    rng = SeededRNG(
        *payload[0],
        **payload[1],
        hash_func=hash_func,
    )
    assert dtype(rng) == to_type[payload_id][dtype][hash_func.__name__]


@pytest.mark.parametrize("payload", payloads)
@pytest.mark.parametrize("hash_func", hash_funcs)
def test_eq_seed(hash_func, payload):
    """Test eq."""
    rng1 = SeededRNG(
        *payload[0],
        **payload[1],
        hash_func=hash_func,
    )
    rng2 = SeededRNG(
        *payload[0],
        **payload[1],
        hash_func=hash_func,
    )
    assert rng1 == rng2


@pytest.mark.parametrize("payload", payloads)
@pytest.mark.parametrize("hash_func", hash_funcs)
@pytest.mark.parametrize("dtype", [bytes, int])
def test_eq_type(dtype, hash_func, payload):
    """Test eq."""
    payload_id = payloads.index(payload)
    rng = SeededRNG(
        *payload[0],
        **payload[1],
        hash_func=hash_func,
    )
    assert rng == to_type[payload_id][dtype][hash_func.__name__]


################################################################
@pytest.mark.parametrize("payload", payloads)
@pytest.mark.parametrize("hash_func", hash_funcs)
@pytest.mark.parametrize("dtype", [bytes, int])
def test_from_type(dtype, hash_func, payload):
    """Test creating RNG from int and bytes."""
    payload_id = payloads.index(payload)
    rng = SeededRNG(
        *payload[0],
        **payload[1],
        hash_func=hash_func,
    )
    seed_data = to_type[payload_id][dtype][hash_func.__name__]
    funcs_from = {
        bytes: SeededRNG.from_bytes,
        int: SeededRNG.from_int,
    }

    assert rng == funcs_from[dtype](seed_data, hash_func=hash_func)


################################################################
def test_randint():
    """Roll int."""
    assert prep_rng.randint(a=0, b=100) == 12


def test_randfloat():
    """Roll float."""
    assert prep_rng.randfloat(a=0, b=10, step=0.1) == 1.2


def test_randbool():
    """Roll bool."""
    assert prep_rng.randbool() is False


def test_randbyte():
    """Roll byte."""
    assert prep_rng.randbyte() == b"o"


################################################################
@pytest.mark.parametrize("hash_func", hash_funcs)
def test_unordered(hash_func):
    """Test RNG with unordered params."""
    rng1 = SeededRNG(b"First", b"Second", hash_func=hash_func)
    rng2 = SeededRNG(b"Second", b"First", hash_func=hash_func)
    assert rng1 == rng2


@pytest.mark.parametrize("hash_func", hash_funcs)
def test_ordered(hash_func):
    """Test RNG with ordered params."""
    rng1 = SeededRNG(ordered=[b"First_ord", b"Second_ord"], hash_func=hash_func)
    rng2 = SeededRNG(ordered=[b"Second_ord", b"First_ord"], hash_func=hash_func)
    assert rng1 != rng2


@pytest.mark.parametrize("hash_func", hash_funcs)
def test_unordered_ordered(hash_func):
    """Test RNG with ordered AND unordered params."""
    rng1 = SeededRNG(
        b"First", b"Second", ordered=[b"First_ord", b"Second_ord"], hash_func=hash_func
    )
    rng2 = SeededRNG(
        b"First", b"Second", ordered=[b"Second_ord", b"First_ord"], hash_func=hash_func
    )
    assert rng1 != rng2


@pytest.mark.parametrize("hash_func", hash_funcs)
def test_zeros(hash_func):
    """Test blank RNG."""
    seed = SeededRNG(hash_func=hash_func)._seed
    assert seed == hash_func().digest_size * b"\x00"
