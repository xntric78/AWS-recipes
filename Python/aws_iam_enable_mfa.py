#!/usr/bin/env python

# Import opinel
from opinel.utils import *
from opinel.utils_iam import *

# Import stock packages
import sys


########################################
##### Main
########################################

def main(args):

    # Configure the debug level
    configPrintException(args.debug)

    # Check version of opinel
    if not check_opinel_version('1.0.4'):
        return 42

    # Arguments
    profile_name = args.profile[0]
    user_name = args.user_name[0]

    # Search for AWS credentials
    credentials = read_creds(profile_name)
    if not credentials['AccessKeyId']:
        return 42

    # Connect to IAM
    iam_client = connect_iam(credentials)
    if not iam_client:
        return 42

    # Set the user name
    if not user_name:
        printInfo('Searching for username...')
        user_name = fetch_from_current_user(iam_client, credentials['AccessKeyId'], 'UserName')
        if not user_name:
            printInfo('Error: could not find user name to enable MFA for.')
            return 42

    # Create an MFA device
    credentials['SerialNumber'] = enable_mfa(iam_client, user_name)

    # Update the no-mfa credentials file
    write_creds_to_aws_credentials_file(profile_name, credentials)
    printInfo('Your credentials file has been updated; you may now use aws_recipes_init_sts_session.py to access the API using short-lived credentials.')


########################################
##### Additional arguments
########################################

default_args = read_profile_default_args(parser.prog)

add_iam_argument(parser, default_args, 'user-name')

########################################
##### Parse arguments and call main()
########################################

args = parser.parse_args()

if __name__ == '__main__':
    sys.exit(main(args))
