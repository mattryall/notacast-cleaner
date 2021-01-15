import io
import logging
import pathlib
import zipfile

import boto3

logger = logging.getLogger(__name__)


def zip_source(src_path: pathlib.Path, include_pattern="**/*.py") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as out:
        for src_file in src_path.glob(include_pattern):
            arc_name = src_file.relative_to(src_path)
            logger.info("Adding: %s -> %s", src_file, arc_name)
            out.write(src_file, arcname=arc_name)
    return buf.getvalue()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(name)s %(message)s')

    zip_buffer = zip_source(pathlib.Path("src"))

    logger.info("Updating lambda...")
    client = boto3.client('lambda')
    client.update_function_code(
        FunctionName='arn:aws:lambda:ap-southeast-2:809899173738:function:notacast-clean',
        ZipFile=zip_buffer,
    )
    logger.info('Updated lambda successfully')


if __name__ == '__main__':
    main()
